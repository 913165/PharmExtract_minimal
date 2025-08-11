#!/usr/bin/env python3
"""End-to-end validation tests for radiology report structuring.

This module provides focused validation tests that verify the complete
RadiologyReportStructurer pipeline by comparing actual processing
results against known good cached outputs.

Typical usage example:

  # Run with unittest (built-in)
  python test_validation.py
  python -m unittest test_validation.py -v
  
  # Run with pytest (recommended for CI/CD)
  pytest test_validation.py -v
"""

import json
import os
import sys
import unittest
from typing import Any
from unittest import mock

# Add the current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from structure_report import RadiologyReportStructurer


class TestRadiologyReportEndToEnd(unittest.TestCase):
    """End-to-end tests for complete RadiologyReportStructurer pipeline."""

    cache_file: str
    sample_data: dict[str, Any]
    structurer: RadiologyReportStructurer

    @classmethod
    def setUpClass(cls):
        cls.cache_file = 'cache/sample_cache.json'
        cls.sample_data = cls._load_sample_cache()
        cls.structurer = RadiologyReportStructurer(
            api_key='test_key', model_id='gemini-2.5-flash'
        )

    @classmethod
    def _load_sample_cache(cls) -> dict[str, Any]:
        if not os.path.exists(cls.cache_file):
            raise FileNotFoundError(f'Sample cache file not found: {cls.cache_file}')

        with open(cls.cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _validate_response_structure(self, response: dict[str, Any]) -> None:
        self.assertIn('segments', response)
        self.assertIn('text', response)
        self.assertIsInstance(response['segments'], list)
        self.assertIsInstance(response['text'], str)

    def _validate_successful_response(self, response: dict[str, Any]) -> None:
        self._validate_response_structure(response)
        self.assertGreater(len(response['segments']), 0)
        self.assertGreater(len(response['text']), 0)

        for segment in response['segments']:
            self._validate_segment_structure(segment)

    def _validate_segment_structure(self, segment: dict[str, Any]) -> None:
        required_fields = ['type', 'label', 'content', 'intervals']
        for field in required_fields:
            self.assertIn(field, segment)

        valid_types = ['prefix', 'body', 'suffix']
        self.assertIn(segment['type'], valid_types)

        if segment['intervals']:
            for interval in segment['intervals']:
                self.assertIn('startPos', interval)
                self.assertIn('endPos', interval)
                self.assertGreaterEqual(interval['startPos'], 0)
                self.assertGreater(interval['endPos'], interval['startPos'])

    @mock.patch('structure_report.lx.extract')
    def test_end_to_end_processing_pipeline(self, mock_extract):
        mock_result = mock.MagicMock()
        mock_result.extractions = []
        mock_extract.return_value = mock_result

        input_text = 'EXAMINATION: Chest CT\n\nFINDINGS: Normal lungs.\n\nIMPRESSION: No acute findings.'

        response = self.structurer.predict(input_text)

        self._validate_response_structure(response)

        mock_extract.assert_called_once()
        call_args = mock_extract.call_args
        self.assertEqual(call_args[1]['text_or_documents'], input_text)
        self.assertEqual(call_args[1]['model_id'], 'gemini-2.5-flash')

    def test_all_cached_samples_validation(self):
        self.assertGreater(len(self.sample_data), 0, 'No samples found in cache')

        for sample_key, sample in self.sample_data.items():
            with self.subTest(sample=sample_key):
                self._validate_successful_response(sample)

    def test_error_handling_with_invalid_input(self):
        with self.assertRaises(ValueError) as context:
            self.structurer.predict('')
        self.assertIn('Report text cannot be empty', str(context.exception))

        with self.assertRaises(ValueError):
            self.structurer.predict('   \n\t  ')

    def test_error_handling_with_no_api_key(self):
        error_structurer = RadiologyReportStructurer(api_key=None)

        response = error_structurer.predict('EXAMINATION: Test')

        self._validate_response_structure(response)
        self.assertEqual(len(response['segments']), 0)
        self.assertIn('Error processing report', response['text'])

    def test_patch_initialization_on_first_use(self):
        new_structurer = RadiologyReportStructurer()

        self.assertFalse(new_structurer._patches_initialized)

        new_structurer._ensure_patches_initialized()
        self.assertTrue(new_structurer._patches_initialized)

    def test_section_mapping_core_functionality(self):
        self.assertEqual(
            self.structurer._map_section('findings_prefix'),
            self.structurer._map_section('findings_prefix'),
        )

        self.assertIsNone(self.structurer._map_section('invalid_section'))
        self.assertIsNone(self.structurer._map_section(''))

    def test_exam_prefix_stripping(self):
        self.assertEqual(
            self.structurer._strip_exam_prefix('EXAMINATION: Chest CT'), 'Chest CT'
        )

        self.assertEqual(
            self.structurer._strip_exam_prefix('Normal findings'), 'Normal findings'
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
