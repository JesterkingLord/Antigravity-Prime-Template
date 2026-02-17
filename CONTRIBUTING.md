# 🚀 Contributing to Antigravity

Thank you for your interest in contributing! We follow the **B.L.A.S.T.** protocol.

## 1. Fork & Clone
Fork the repo and clone it locally.

## 2. Environment Setup
Run `python antigravity.py health` to ensure your environment is ready.

## 3. Creating a New Skill
Use the CLI wizard:
```bash
python antigravity.py new-skill
```
Follow the prompts to generate the skill structure properly.

## 4. Testing
Always run the test suite before submitting a PR:
```bash
python antigravity.py test
python antigravity.py lint
```

## 5. Commit Standards
Use semantic commit messages:
- `feat: added vector memory`
- `fix: resolved api router bug`
- `docs: updated readme`

## 6. Pull Request
Submit your PR to the `main` branch. The CI pipeline will automatically run tests.
