"""Cache management for pharmaceutical report structuring results.

This module provides the CacheManager class that handles caching of
structured pharmaceutical report results to improve performance and reduce
API calls. Supports both sample-based and custom text caching with
JSON file persistence.

Example usage:

  cache_manager = CacheManager(cache_dir="cache")
  cached_result = cache_manager.get_cached_result(report_text, sample_id)
  if not cached_result:
      result = process_report(report_text)
      cache_manager.cache_result(report_text, result, sample_id)
"""

import hashlib
import json
import logging
import os
import time
from typing import Any

from langextract.data import AnnotatedDocument, CharInterval, Extraction

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages caching of pharmaceutical report structuring results.

    This class provides efficient caching capabilities for structured
    pharmaceutical report results, supporting both file-based persistence
    and in-memory access with automatic cache key generation and management.

    Attributes:
        cache_dir: Directory path for cache storage.
        cache_file: Full path to the cache JSON file.
    """

    def __init__(self, cache_dir: str = "cache"):
        """Initializes the CacheManager with specified cache directory.

        Args:
            cache_dir: Directory path for cache storage. Defaults to "cache".
        """
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(cache_dir, "sample_cache.json")
        self._cache_data: dict[str, Any] = {}
        self._load_cache()

    def _ensure_cache_dir(self):
        """Ensures the cache directory exists, creating it if necessary."""
        os.makedirs(self.cache_dir, exist_ok=True)

    def _load_cache(self):
        """Loads existing cache data from file into memory.

        Attempts to load cache from the JSON file. If the file doesn't
        exist or cannot be loaded, initializes with an empty cache.
        """
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self._cache_data = json.load(f)
                logger.info(f"Loaded cache with {len(self._cache_data)} entries")
            else:
                self._cache_data = {}
                logger.info("No existing cache file found, starting with empty cache")
        except Exception as e:
            logger.error(f"Error loading cache: {e}")
            self._cache_data = {}

    def _save_cache(self):
        """Saves current cache data to the JSON file.

        Ensures the cache directory exists before writing the cache data
        to the JSON file with proper formatting.
        """
        try:
            self._ensure_cache_dir()
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self._cache_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved cache with {len(self._cache_data)} entries")
        except Exception as e:
            logger.error(f"Error saving cache: {e}")

    def _get_cache_key(self, text: str, sample_id: str | None = None) -> str:
        """Generates a cache key for the given text and optional sample ID.

        Args:
            text: The input text to generate a key for.
            sample_id: Optional sample identifier for predefined samples.

        Returns:
            A string cache key, either sample-based or hash-based.
        """
        if sample_id:
            # Avoid double "sample_" prefix if sample_id already starts with "sample_"
            if sample_id.startswith("sample_"):
                return sample_id
            else:
                return f"sample_{sample_id}"
        else:
            return f"custom_{hashlib.md5(text.encode('utf-8')).hexdigest()}"

    def get_cached_result(self, text: str, sample_id: str | None = None) -> dict | None:
        """Gets cached result for given text.

        Args:
            text: The input text to look up.
            sample_id: Optional sample identifier for predefined samples.

        Returns:
            The cached result dictionary if found, None otherwise.
        """
        cache_key = self._get_cache_key(text, sample_id)
        result = self._cache_data.get(cache_key)
        if result:
            logger.info(f"Cache hit for key: {cache_key}")
        return result

    def _dict_to_extraction(self, extraction_dict: dict[str, Any]) -> Extraction:
        """Converts a cached extraction dictionary to an Extraction object."""
        char_interval = None
        if extraction_dict.get("char_interval"):
            interval_data = extraction_dict["char_interval"]
            char_interval = CharInterval(
                start_pos=interval_data.get("start_pos"),
                end_pos=interval_data.get("end_pos"),
            )

        return Extraction(
            extraction_text=extraction_dict.get("extraction_text", ""),
            extraction_class=extraction_dict.get("extraction_class", ""),
            attributes=extraction_dict.get("attributes", {}),
            char_interval=char_interval,
            alignment_status=extraction_dict.get("alignment_status"),
        )

    def convert_cached_response_to_annotated_document(
        self, cached_response: dict[str, Any]
    ) -> AnnotatedDocument:
        """Converts a cached response to an AnnotatedDocument with proper Extraction objects."""
        extractions = []
        if (
            "annotated_document_json" in cached_response
            and "extractions" in cached_response["annotated_document_json"]
        ):
            for extraction_dict in cached_response["annotated_document_json"][
                "extractions"
            ]:
                extractions.append(self._dict_to_extraction(extraction_dict))

        return AnnotatedDocument(text="", extractions=extractions)

    def cache_result(
        self, text: str, result: dict[str, Any] | Any, sample_id: str | None = None
    ) -> None:
        """Caches result for given text.

        Args:
            text: The input text to cache results for.
            result: The structured result dictionary to cache.
            sample_id: Optional sample identifier for predefined samples.
        """
        cache_key = self._get_cache_key(text, sample_id)
        self._cache_data[cache_key] = result
        self._save_cache()
        logger.info(f"Cached result for key: {cache_key}")

    def clear_cache(self) -> None:
        """Clears all cached results and saves the empty cache to file."""
        self._cache_data = {}
        self._save_cache()
        logger.info("Cache cleared")

    def remove_sample(self, sample_id: str) -> bool:
        """Removes a specific sample from cache.

        Args:
            sample_id: The sample identifier to remove.

        Returns:
            True if the sample was found and removed, False otherwise.
        """
        cache_key = f"sample_{sample_id}"
        if cache_key in self._cache_data:
            del self._cache_data[cache_key]
            self._save_cache()
            logger.info(f"Removed sample {sample_id} from cache")
            return True
        else:
            logger.warning(f"Sample {sample_id} not found in cache")
            return False

    def prepopulate_cache_with_samples(
        self,
        sample_reports: list[dict[str, Any]],
        structurer_callable,
        force_refresh: bool = False,
    ) -> None:
        """Prepopulates cache with sample reports.

        Processes a list of sample reports and caches their structured
        results to improve initial application performance. Includes rate
        limiting and error handling for robust cache population.

        Args:
            sample_reports: List of sample report dictionaries with 'id' and 'text'.
            structurer_callable: Function to call for structuring reports.
            force_refresh: If True, reprocesses samples even if already cached.
        """
        if not sample_reports:
            logger.info("No sample reports provided for cache prepopulation")
            return

        logger.info(f"Starting cache prepopulation with {len(sample_reports)} samples")

        lock_file = os.path.join(self.cache_dir, ".cache_lock")
        if os.path.exists(lock_file) and not force_refresh:
            logger.info("Cache prepopulation already in progress or recently completed")
            return

        try:
            self._ensure_cache_dir()
            with open(lock_file, "w") as f:
                f.write(str(os.getpid()))

            for i, sample in enumerate(sample_reports):
                sample_id = sample.get("id")
                sample_text = sample.get("text", "")

                if not sample_id or not sample_text:
                    logger.warning(f"Sample {i} missing id or text, skipping")
                    continue

                if not force_refresh and self.get_cached_result(sample_text, sample_id):
                    logger.info(f"Sample {sample_id} already cached, skipping")
                    continue

                logger.info(
                    f"Processing sample {sample_id} ({i+1}/{len(sample_reports)})"
                )

                try:
                    result = structurer_callable(sample_text)
                    self.cache_result(sample_text, result, sample_id)
                    logger.info(f"Successfully cached sample {sample_id}")
                except Exception as e:
                    logger.error(f"Error processing sample {sample_id}: {e}")
                    continue

                time.sleep(6)

            logger.info("Cache prepopulation completed")
            self._save_cache()

        except Exception as e:
            logger.error(f"Error during cache prepopulation: {e}")
        finally:
            if os.path.exists(lock_file):
                os.remove(lock_file)

    def get_cache_stats(self) -> dict[str, Any]:
        """Gets cache statistics.

        Returns:
            Dictionary containing cache statistics including entry counts,
            file information, and cache status details.
        """
        sample_count = sum(
            1 for key in self._cache_data.keys() if key.startswith("sample_")
        )
        custom_count = sum(
            1 for key in self._cache_data.keys() if key.startswith("custom_")
        )

        return {
            "total_entries": len(self._cache_data),
            "sample_entries": sample_count,
            "custom_entries": custom_count,
            "cache_file": self.cache_file,
            "cache_file_exists": os.path.exists(self.cache_file),
        }
