#!/usr/bin/env python3
"""Utility script to rebuild the demonstration cache with current structurer output.

This development tool rebuilds the cache using the current
RadiologyReportStructurer implementation, ensuring that cached results
include the latest features such as raw_prompt data. The script processes
all sample reports from the static JSON file and caches their structured
results for improved demo performance.

The script requires the KEY environment variable to be set with a valid
Gemini API key and optionally accepts MODEL_ID to specify which model
to use for processing.

Usage:
    export KEY=your_gemini_api_key_here
    export MODEL_ID=gemini-2.5-pro  # optional, defaults to gemini-2.5-pro
    python tools/rebuild_cache.py
"""
import json
import os
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent.parent))

from cache_manager import CacheManager
from structure_report import RadiologyReportStructurer

API_KEY = os.environ.get("KEY")
if not API_KEY:
    sys.exit("KEY environment variable not set. Export KEY before running.")

SAMPLES_PATH = Path("static/sample_reports.json")
if not SAMPLES_PATH.exists():
    sys.exit("static/sample_reports.json not found")

samples = json.loads(SAMPLES_PATH.read_text())["samples"]

MODEL_ID = os.environ.get("MODEL_ID", "gemini-2.5-pro")
structurer = RadiologyReportStructurer(api_key=API_KEY, model_id=MODEL_ID)

import time

cache = CacheManager(cache_dir="cache")

print("Clearing existing cache...")
cache.clear_cache()

print(f"Processing {len(samples)} samples with {MODEL_ID}...")
for s in samples:
    sid = s["id"]
    text = s["text"]
    print(f"  Processing {sid}...")

    retries = 0
    while retries < 5:
        try:
            result = structurer.predict(text)
            cache.cache_result(text, result, sample_id=sid)
            break
        except Exception as e:
            retries += 1
            print(f"    Warning: {e}. Retry {retries}/5...")
            time.sleep(5)
    else:
        print(f"    Error: Failed to process {sid} after 5 retries, skipping.")
    time.sleep(3)  # base throttle

print("Cache rebuild completed successfully.")
