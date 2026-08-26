# Contributing to CyberNova Lab

Thank you for helping make beginner cybersecurity education friendlier. First-time contributors are especially welcome.

## Before you begin

- Be respectful and follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- Keep features educational and defensive.
- Never include real passwords, private keys, personal data, malware, exploit code, or targets you do not own.
- For a large change, open an issue before writing code so the idea can be discussed.

## Local setup

```bash
git clone https://github.com/sansw123/cybernova-lab.git
cd cybernova-lab
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS or Linux
source .venv/bin/activate
```

Then install and test:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Make a contribution

1. Fork this repository.
2. Create a focused branch: `git switch -c feature/short-name`.
3. Make one understandable change.
4. Add or update tests and documentation.
5. Run the test suite.
6. Commit clearly: `git commit -m "feat: add quiz difficulty levels"`.
7. Push your branch and open a pull request.

Useful commit prefixes are `feat:`, `fix:`, `docs:`, `test:`, and `chore:`.

## Definition of done

- The change is safe, understandable, and within project scope.
- Existing tests pass and new behaviour has a test.
- User-facing behaviour is documented.
- No secrets, generated files, or personal data are committed.
- The pull-request template is completed.

Small, thoughtful pull requests are easier to review than large ones. Asking questions is part of contributing.
