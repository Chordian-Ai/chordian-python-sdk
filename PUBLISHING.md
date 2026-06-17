# Publishing the `chordian` package

This guide covers publishing to **TestPyPI first** (a safe sandbox), then to the **real PyPI**.

> TestPyPI and PyPI are separate registries with separate accounts and tokens.

## 0. One-time prerequisites

Install the build tooling (already included in the `dev` extra):

```bash
pip install --upgrade build twine
```

Create accounts and **API tokens**:

- TestPyPI: https://test.pypi.org/account/register/ → then https://test.pypi.org/manage/account/token/
- PyPI:     https://pypi.org/account/register/      → then https://pypi.org/manage/account/token/

Tokens look like `pypi-AgEI...`. When uploading, the username is always `__token__` and the
password is the token.

## 1. Bump the version

Edit [`chordian/version.py`](chordian/version.py) (e.g. `0.1.0` → `0.1.1`) and update
[`CHANGELOG.md`](CHANGELOG.md). PyPI **rejects re-uploading an existing version**, so every
upload needs a new version number.

## 2. Build the distributions

```bash
# from the repo root
rm -rf dist
python -m build
```

This produces `dist/chordian-<version>.tar.gz` (sdist) and
`dist/chordian-<version>-py3-none-any.whl` (wheel).

## 3. Validate

```bash
python -m twine check dist/*
```

## 4. Upload to TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
# username: __token__
# password: <your TestPyPI token>
```

Then install from TestPyPI in a clean virtualenv to verify it works. The extra index is needed
so real dependencies (e.g. `httpx`) resolve from the real PyPI:

```bash
python -m venv /tmp/chordian-test && source /tmp/chordian-test/bin/activate
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            chordian
python -c "import chordian; print(chordian.__version__)"
```

## 5. Upload to the real PyPI

When you're happy:

```bash
python -m twine upload dist/*
# username: __token__
# password: <your PyPI token>
```

Verify:

```bash
pip install chordian
```

## Optional: store credentials in `~/.pypirc`

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-XXXX

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YYYY
```

With this file you can drop the interactive prompts:
`python -m twine upload --repository testpypi dist/*`.

## Optional: automated publishing via GitHub Actions

[`.github/workflows/publish.yml`](.github/workflows/publish.yml) builds and uploads on a Git tag.
The recommended, token-free setup is **PyPI Trusted Publishing** (OpenID Connect):

1. On PyPI/TestPyPI, add a *pending publisher* pointing at this repo and the `publish.yml` workflow.
2. Tag a release and push:

   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

Alternatively, store a token as the `PYPI_API_TOKEN` (and `TEST_PYPI_API_TOKEN`) repository secret
and the workflow will use it.

---

## Creating the public GitHub repository

The SDK is initialised as a local Git repo. To publish it publicly:

```bash
# Using the GitHub CLI (creates the repo and pushes in one step):
gh repo create chordian-python --public --source=. --remote=origin --push

# Or manually, after creating an empty repo on github.com:
git remote add origin https://github.com/<org>/chordian-python.git
git branch -M main
git push -u origin main
```
