# Contributing to instagram-private-api

Thank you for your interest in contributing to the project. We welcome bug reports, endpoint additions, and documentation improvements.

---

## Development Guidelines

### Code Style & Architecture
- **Python**: Follow PEP 8 guidelines. Type hints are mandatory. Keep dependencies minimal.
- **TypeScript**: Strict TypeScript mode enabled. All public APIs must have complete `.d.ts` type exports.
- **No Emojis**: Do not use emojis in code, docstrings, or commit messages.

### Testing
- Ensure all Python tests pass before opening a PR:
  ```bash
  python -m pytest tests/ -v
  ```
- Ensure TypeScript builds with zero compiler errors:
  ```bash
  cd ts
  npm run build
  ```

### Pull Request Process
1. Fork the repository and create your branch from `main`.
2. Add comprehensive unit tests covering any new endpoints or models.
3. Keep commits atomic and descriptive following Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`).
4. Submit your pull request with a clear description of the problem solved.

### Commercial & Enterprise Inquiries
For private cluster access or custom signing daemons, reach out directly to [@mxmtkchk](https://t.me/mxmtkchk) on Telegram.
