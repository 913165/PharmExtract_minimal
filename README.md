---
title: PharmExtract
emoji: 💊
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: apache-2.0
header: mini
app_port: 7870
tags:
  - medical
  - nlp
  - pharmaceutical
  - pharmextract
  - gemini
  - structured-data
---

# PharmExtract: Pharmaceutical Report Structuring Demo

A demonstration application powered by [LangExtract](https://github.com/google/langextract) that structures pharmaceutical reports using Gemini models. Transform unstructured pharmaceutical documents into organized, interactive segments with regulatory and clinical significance annotations.

## Try the Demo

Transform unstructured pharmaceutical reports into structured data with highlighted sections that are precisely mapped back to the original source text.

## Key Features

- **Structured Output**: Organizes reports into document header, methodology, results, and conclusions sections
- **Interactive Highlighting**: Click any section to see its exact source in the original text
- **Regulatory Significance**: Annotates sections with regulatory and clinical context
- **Character-Level Mapping**: Precise attribution back to source text
- **Multi-Model Support**: Gemini 2.5 Flash (fast) and Pro (comprehensive)

## Quick Start

### Setup

```bash
git clone <your-repo-url>
cd pharmextract
python -m venv venv
source venv/bin/activate
```

### Local Development

```bash
source venv/bin/activate
export KEY=your_gemini_api_key_here
python main.py
```

Access at: http://localhost:7870

## API Usage

### Example Request
```bash
curl -X POST \
  -H 'X-Model-ID: gemini-2.5-flash' \
  -H 'X-Use-Cache: true' \
  -d 'FINDINGS: Normal heart and lungs. IMPRESSION: Normal study.' \
  http://localhost:7870/predict
```

### Response Format
```json
{
  "segments": [{
    "type": "body",
    "label": "Chest", 
    "content": "Normal heart and lungs",
    "intervals": [{"startPos": 10, "endPos": 32}],
    "significance": "minor"
  }],
  "text": "Chest:\n- Normal heart and lungs",
  "annotated_document_json": {...}
}
```

## Architecture

- **Backend**: Flask + Python 3.10+ with full type safety
- **NLP Engine**: [LangExtract](https://github.com/google/langextract) for structured extraction
- **AI Models**: Google Gemini 2.5 (Flash/Pro)
- **Frontend**: Vanilla JavaScript with interactive UI
- **Deployment**: Docker + Hugging Face Spaces
- **Package Details**: See [pyproject.toml](https://huggingface.co/spaces/google/radextract/blob/main/pyproject.toml) for dependencies, metadata, and tooling

## Project Structure

```
pharmextract/
├── app.py                 # Flask API endpoints
├── structure_report.py    # Core structuring logic
├── sanitize.py           # Text preprocessing & normalization
├── prompt_instruction.py  # LangExtract prompt
├── cache_manager.py      # Response caching
├── static/               # Frontend assets
└── templates/            # HTML templates
```

## Development

### Setup
```bash
git clone <your-repo-url>
cd pharmextract
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Code Quality
```bash
# Format code
pyink . && isort .

# Type checking
mypy . --ignore-missing-imports

# Run tests
pytest
```

### Docker
```bash
# Build and run
docker build -t pharmextract .
docker run -p 7870:7870 --env-file env.list pharmextract
```

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Related Projects

- **[LangExtract](https://github.com/google/langextract)**: Core NLP library

---

**Built for the medical AI community** | **Hosted on Hugging Face Spaces**

## Disclaimer

This is not an officially supported Google product. If you use PharmExtract or LangExtract in production or publications, please cite accordingly and acknowledge usage. Use is subject to the [Apache 2.0 License](LICENSE). For health-related applications, use of LangExtract is also subject to the [Health AI Developer Foundations Terms of Use](https://developers.google.com/health-ai-foundations/terms).
# PharmExtract
# PharmExtract
# PharmExtract_minimal
