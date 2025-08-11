"""Test suite for Flask application endpoints and integration.

This module provides comprehensive tests for the Flask application including
route testing, model integration, caching behavior, and error handling.

Run with: python test_app.py or pytest test_app.py
"""

import json
import os
import unittest
from unittest import mock

# Mock the environment before importing app to avoid initialization errors
with mock.patch.dict(os.environ, {'KEY': 'test_api_key_for_import'}):
    from main import Model, app, setup_cache


class TestFlaskApplication(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_client = app.test_client()
        app.config['TESTING'] = True

    def test_index_route_returns_html(self):
        response = self.test_client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)

    def test_cache_stats_route(self):
        response = self.test_client.get('/cache/stats')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        data = json.loads(response.data)
        self.assertIsInstance(data, dict)

    @mock.patch('app.model.predict')
    def test_predict_route_with_valid_data(self, mock_predict):
        mock_predict.return_value = {
            'segments': [{'type': 'body', 'content': 'test'}],
            'text': 'test output',
        }

        response = self.test_client.post('/predict', data='FINDINGS: Normal chest CT')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn('segments', data)
        self.assertIn('text', data)

    def test_predict_route_with_empty_data(self):
        response = self.test_client.post('/predict', data='')
        self.assertEqual(response.status_code, 400)

        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Empty input')
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Input text is required')
        self.assertIn('max_length', data)

    @mock.patch('app.model.predict')
    def test_predict_with_custom_headers(self, mock_predict):
        mock_predict.return_value = {'segments': [], 'text': 'test'}

        headers = {
            'X-Use-Cache': 'false',
            'X-Sample-ID': 'test_sample',
            'X-Model-ID': 'gemini-2.5-flash',
        }

        response = self.test_client.post(
            '/predict', data='Test report', headers=headers
        )
        self.assertEqual(response.status_code, 200)
        mock_predict.assert_called_once_with('Test report', model_id='gemini-2.5-flash')

    @mock.patch('app.cache_manager.get_cached_result')
    def test_predict_with_cache_hit(self, mock_get_cached):
        cached_response = {
            'segments': [{'type': 'body', 'content': 'cached'}],
            'text': 'cached result',
        }
        mock_get_cached.return_value = cached_response

        response = self.test_client.post(
            '/predict', data='Test report', headers={'X-Use-Cache': 'true'}
        )

        data = json.loads(response.data)
        self.assertTrue(data.get('from_cache'))
        self.assertIn('segments', data)


class TestModelClass(unittest.TestCase):

    @mock.patch.dict(os.environ, {'KEY': 'test_api_key'})
    def test_model_initialization_with_api_key(self):
        model = Model()
        self.assertEqual(model.gemini_api_key, 'test_api_key')
        self.assertIn('gemini-2.5-flash', model._structurers)

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_model_initialization_without_api_key(self):
        with self.assertRaises(ValueError) as context:
            Model()
        self.assertIn('KEY environment variable not set', str(context.exception))

    @mock.patch.dict(os.environ, {'KEY': 'test_key', 'MODEL_ID': 'custom-model'})
    def test_model_initialization_with_custom_model(self):
        model = Model()
        self.assertIn('custom-model', model._structurers)

    @mock.patch.dict(os.environ, {'KEY': 'test_key'})
    @mock.patch('app.RadiologyReportStructurer')
    def test_get_structurer_creates_new_instance(self, mock_structurer_class):
        model = Model()
        model._get_structurer('new-model')

        # Should be called twice: once for default, once for new model
        self.assertEqual(mock_structurer_class.call_count, 2)

    @mock.patch.dict(os.environ, {'KEY': 'test_key'})
    @mock.patch('app.RadiologyReportStructurer')
    def test_predict_calls_structurer(self, mock_structurer_class):
        mock_instance = mock.Mock()
        mock_instance.predict.return_value = {'result': 'test'}
        mock_structurer_class.return_value = mock_instance

        model = Model()
        result = model.predict('test data', 'test-model')

        mock_instance.predict.assert_called_once_with('test data')
        self.assertEqual(result, {'result': 'test'})


class TestCacheSetup(unittest.TestCase):

    @mock.patch('os.path.exists')
    @mock.patch('shutil.copy2')
    @mock.patch('os.makedirs')
    def test_setup_cache_copies_existing_file(
        self, mock_makedirs, mock_copy, mock_exists
    ):
        mock_exists.return_value = True

        cache_dir = setup_cache()

        mock_makedirs.assert_called_once_with('/tmp/cache', exist_ok=True)
        mock_copy.assert_called_once()
        self.assertEqual(cache_dir, '/tmp/cache')

    @mock.patch('os.path.exists')
    @mock.patch('os.makedirs')
    def test_setup_cache_handles_missing_source(self, mock_makedirs, mock_exists):
        mock_exists.return_value = False

        cache_dir = setup_cache()

        mock_makedirs.assert_called_once_with('/tmp/cache', exist_ok=True)
        self.assertEqual(cache_dir, '/tmp/cache')


class TestErrorHandling(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_client = app.test_client()
        app.config['TESTING'] = True

    def setUp(self):
        # Suppress all logging during error tests to reduce noise
        import logging

        logging.disable(logging.CRITICAL)

    def tearDown(self):
        # Re-enable logging
        import logging

        logging.disable(logging.NOTSET)

    @mock.patch('app.model.predict')
    @mock.patch('app.logger')
    def test_predict_handles_type_error(self, mock_logger, mock_predict):
        mock_predict.side_effect = TypeError('Invalid type')

        response = self.test_client.post('/predict', data='Test data')
        self.assertEqual(response.status_code, 500)

        data = json.loads(response.data)
        self.assertIn('Processing error', data['error'])

    @mock.patch('app.model.predict')
    @mock.patch('app.logger')
    def test_predict_handles_general_exception(self, mock_logger, mock_predict):
        mock_predict.side_effect = Exception('General error')

        response = self.test_client.post('/predict', data='Test data')
        self.assertEqual(response.status_code, 500)

        data = json.loads(response.data)
        self.assertIn('General error', data['error'])


if __name__ == '__main__':
    unittest.main()
