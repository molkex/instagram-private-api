# Contributing Guidelines

Thank you for your interest in contributing to `instagram-private-api`.

## Development Setup

### Python Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/
```

### TypeScript / Node.js Environment

```bash
cd ts
npm install
npm run build
```

## Guidelines

1. **Strict Mobile Protocol Parity**: All endpoints must match official Meta iOS or Android requests. Do not use legacy web scrapers or unauthenticated endpoints where authenticated mobile endpoints exist.
2. **Deterministic Typing**: Ensure all Python endpoints expose typed dataclasses and all TypeScript modules compile with zero warnings under `strict: true`.
3. **No Hardcoded Secrets**: Never commit real session cookies, passwords, or personal API keys.
4. **Code Style**: Format Python with `black` / `ruff`, TypeScript with standard conventions.
