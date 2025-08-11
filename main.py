"""Flask web application for radiology report structuring using Gemini models.

This module provides a web API that structures radiology reports into
semantic sections using LangExtract and Google's Gemini language models.
The application supports caching, multiple model configurations, and
provides both a web interface and REST API endpoints.

Typical usage example:

  # Set environment variables
  export KEY=your_gemini_api_key_here
  export MODEL_ID=gemini-2.5-flash
  
  # Run the application
  python main.py
"""

import logging
import os
import shutil
import tempfile
import time
import json
import hashlib

from flask import Flask, jsonify, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from cache_manager import CacheManager
from sanitize import preprocess_report
from social_sharing import SocialSharingConfig
from structure_report import RadiologyReportStructurer, ResponseDict

# Configuration constants
MAX_INPUT_LENGTH = 3000

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class Model:
    """Manages RadiologyReportStructurer instances for different Gemini model IDs.

    This class handles initialization, caching, and coordination
    of structurer instances for various model configurations, ensuring
    efficient resource usage and consistent API key management.
    """

    def __init__(self):
        """Initializes the Model manager with default structurer.

        Sets up the Gemini API key from environment variables
        and creates a default structurer instance for the configured model.

        Raises:
            ValueError: If the KEY environment variable is not set.
        """
        self.gemini_api_key = os.environ.get("KEY")
        if not self.gemini_api_key:
            logger.error("KEY environment variable not set.")
            raise ValueError("KEY environment variable not set.")

        self._structurers: dict[str, RadiologyReportStructurer] = {}

        default_model_id = os.environ.get("MODEL_ID", "gemini-2.5-flash")
        self._structurers[default_model_id] = RadiologyReportStructurer(
            api_key=self.gemini_api_key,
            model_id=default_model_id,
        )

        logger.info(
            f"RadExtract ready [Worker {os.getpid()}] with model: {default_model_id}"
        )

    def _get_structurer(self, model_id: str) -> RadiologyReportStructurer:
        """Returns a cached or newly created structurer for the given model ID.

        Args:
            model_id: Identifier for the specific model configuration.

        Returns:
            RadiologyReportStructurer instance for the specified model.
        """
        if model_id not in self._structurers:
            logger.info(f"Creating structurer for model: {model_id}")
            self._structurers[model_id] = RadiologyReportStructurer(
                api_key=self.gemini_api_key,
                model_id=model_id,
            )
        return self._structurers[model_id]

    def predict(self, data: str, model_id: str) -> ResponseDict:
        """Processes prediction request using the specified model.

        Args:
            data: Input text data to be processed.
            model_id: Identifier for the model to use for processing.

        Returns:
            Dictionary containing the structured prediction results.
        """
        logger.info(f"Processing prediction with model..: {model_id}")
        structurer = self._get_structurer(model_id)
        result = structurer.predict(data)
        logger.info(f"Result preview: {str(result)[:500]}...")
        return result


model = Model()


# Copy prebuilt cache to writable location if it exists
def setup_cache():
    """Sets up the cache directory and copies prebuilt cache files.

    Creates a writable cache directory in /tmp and copies any existing
    prebuilt cache files to ensure the latest version is available.

    Returns:
        Path to the configured cache directory.
    """
    cache_dir = tempfile.gettempdir() + "/cache"
    os.makedirs(cache_dir, exist_ok=True)

    source_cache = "cache/sample_cache.json"
    target_cache = os.path.join(cache_dir, "sample_cache.json")

    if os.path.exists(source_cache) and not os.path.exists(target_cache):
        shutil.copy2(source_cache, target_cache)
        logger.info(f"Initialized cache with {os.path.getsize(target_cache)} bytes")

    return cache_dir


cache_dir = setup_cache()
cache_manager = CacheManager(cache_dir=cache_dir)

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
    template_folder="templates",
)

# Initialize rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[
        os.environ.get("RATE_LIMIT_DAY", "200 per day"),
        os.environ.get("RATE_LIMIT_HOUR", "50 per hour"),
    ],
    storage_uri="memory://",
)


@app.route("/")
def index():
    """Renders the main application interface.

    Returns:
        Rendered HTML template for the application index page.
    """
    # Get social sharing context
    social_context = SocialSharingConfig.get_sharing_context(request.url_root)

    return render_template("index.html", **social_context)


@app.route("/cache/stats")
def cache_stats():
    """Returns cache performance statistics.

    Returns:
        JSON response containing cache usage and performance statistics.
    """
    return jsonify(cache_manager.get_cache_stats())


@app.route("/predict", methods=["POST"])
@limiter.limit(os.environ.get("RATE_LIMIT_PREDICT", "100 per hour"))
def predict():
    """Processes radiology report text and returns structured results.

    Accepts raw text via POST request body with optional headers
    for caching, sample identification, and model selection. Supports
    both cached and real-time processing modes.

    Returns:
        JSON response containing structured report segments, annotations,
        and formatted text. Includes cache status when applicable.

    Raises:
        500: If processing fails due to invalid input or model errors.
    """
    start_time = time.time()

    try:
        data = request.get_data(as_text=True)

        # Validate input to ensure it meets API requirements
        if not data or not data.strip():
            return (
                jsonify(
                    {
                        "error": "Empty input",
                        "message": "Input text is required",
                        "max_length": MAX_INPUT_LENGTH,
                    }
                ),
                400,
            )

        if len(data) > MAX_INPUT_LENGTH:
            return (
                jsonify(
                    {
                        "error": "Input too long",
                        "message": f"Input length ({len(data)} characters) exceeds maximum allowed length of {MAX_INPUT_LENGTH} characters",
                        "max_length": MAX_INPUT_LENGTH,
                    }
                ),
                400,
            )

        use_cache = request.headers.get("X-Use-Cache", "true").lower() == "true"
        sample_id = request.headers.get("X-Sample-ID")
        model_id = request.headers.get(
            "X-Model-ID", os.environ.get("MODEL_ID", "gemini-2.5-flash")
        )
        processed_data = preprocess_report(data)

        if use_cache:
            cached_result = cache_manager.get_cached_result(processed_data, sample_id)
            if cached_result:
                # Ensure 'text' field is always present for frontend compatibility
                if 'text' not in cached_result:
                    cached_result['text'] = ''
                req_id = hashlib.md5(
                    f"{request.remote_addr}{int(time.time()/3600)}".encode()
                ).hexdigest()[:8]
                logger.info(
                    f"🟢 CACHE HIT [Req {req_id}] [Worker {os.getpid()}] - Returning cached result (no API call)"
                )
                return jsonify({"from_cache": True, **cached_result})

        try:
            req_id = hashlib.md5(
                f"{request.remote_addr}{int(time.time()/3600)}".encode()
            ).hexdigest()[:8]
            logger.info(
                f"🔴 API CALL [Req {req_id}] [Worker {os.getpid()}] - Processing with Gemini model: {model_id}"
            )
            result = model.predict(processed_data, model_id=model_id)

            if use_cache:
                cache_manager.cache_result(processed_data, result, sample_id)

            result["sanitized_input"] = processed_data

            return jsonify(result)

        except TypeError as te:
            error_msg = str(te)
            logger.error(f"TypeError in prediction: {error_msg}", exc_info=True)

            return (
                jsonify({"error": "Processing error. Please try a different input."}),
                500,
            )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)

        return jsonify({"error": str(e)}), 500


@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded errors."""
    return (
        jsonify(
            {
                "error": "Rate limit exceeded. Please try again later.",
                "message": str(e.description),
            }
        ),
        429,
    )


if __name__ == "__main__":
    logger.info("Starting development server")
    app.run(host="0.0.0.0", port=7870, debug=True)
