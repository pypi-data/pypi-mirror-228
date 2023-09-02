# Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

## Bug reports

When [reporting a bug](https://https://gitlab.com/ConsenSys/codefi/products/mmi/mmi-sdk-py/xavier.brochard/mmi-sdk-py/issues>) please include:

-   Your operating system name and version.
-   Any details about your local setup that might be helpful in troubleshooting.
-   Detailed steps to reproduce the bug.

## Documentation improvements

`metamask-institutional.sdk` could always use more documentation, whether as part of the
official metamask-institutional.sdk docs, in docstrings, or even on the web in blog posts,
articles, and such.

## Feature requests and feedback

The best way to send feedback is to file an issue at https://gitlab.com/ConsenSys/codefi/products/mmi/mmi-sdk-py/issues.

If you are proposing a feature:

-   Explain in detail how it would work.
-   Keep the scope as narrow as possible, to make it easier to implement.

## Development

Note: The commands we list below use `python` and `pip`. Depending on your local setup, you might need to replace them by `python3` and `pip3`.

### Requirements

-   Python 3.7 or above

### Forking the source code

To set up `mmi-sdk-py` for local development:

1. Fork [mmi-sdk-py](https://gitlab.com/ConsenSys/codefi/products/mmi/mmi-sdk-py) (look for the "Fork" button).
2. Clone your fork locally:

```bash
git clone git@https://gitlab.com/ConsenSys/codefi/products/mmi/mmi-sdk-py:YOURNAME/mmi-sdk-py.git
```

3. Create a branch for local development:

    ```bash
    git checkout -b name-of-your-bugfix-or-feature
    ```

    Now you can make your changes locally.

### Installing dependencies

To install `metamask-institutional.sdk`, along with the tools you need to develop and run tests, run the following:

```bash
$ pip install -e .[dev] # With your default Python version
# or
$ python3.8 -m pip install -e .[dev] # With a specific Python version
```

> Note: In the zsh shell, the command will fail because the pattern `.[dev]` isn't supported. In that case, make sure you run it within an other shell, like bash:

```bash
$ bash
bash-3.2$ pip install -e .[dev]
```

### Unit tests

Run all unit tests with:

```bash
$ pytest src # Against your default Python version
# or
$ python3.8 -m pytest src # Against a specific Python version
```

### End to end tests

A great way to verify the library is to run the various examples scripts.

Copy the file `.env.sample` to `.env`, then replace the values whith your tokens

```bash
$ cp .env.sample .env
```

Then run all examples at once like so:

```bash
$ python e2e/run_examples.py
```

### QA tests

You should also check that you got no packaging issues:

```bash
tox -e check
```

When checking with `tox -e check`, you might receive warnings from `isort` that imports are not properly ordered. To automatically sort your imports with `isort`, run the following:

```bash
pip install isort
isort .
```

To run a complete QA analysis, including unit tests again multiple Python versions, manifest check, and imports order check, run:

```bash
tox
```

### Submitting changes

Commit your changes and push your branch to GitLab:

```bash
git add .
git commit -m "Your detailed description of your changes."
git push origin name-of-your-bugfix-or-feature
```

Submit a pull request through the GitLab website.

#### Pull Request Guidelines

If you need some code review or feedback while you're developing the code just make the pull request.

For merging, you should:

1. Include passing tests (run `tox`).
2. Update documentation when there's new API, functionality etc.
3. Add a note to `CHANGELOG.md` about the changes.
4. Add yourself to `AUTHORS.md`.

### Releasing manually

The GitLab CI handles automatically the release process. We list here the manual steps for reference.

#### Versioning

We use [bump2version](https://pypi.org/project/bump2version/) for SemVer versioning.

```sh
bump2version patch
bump2version minor
bump2version major
```

#### Building

Before building dists make sure you got a clean build area:

```bash
rm -rf build
rm -rf src/*.egg-info
```

Note:

> Dirty `build` or `egg-info` dirs can cause problems: missing or stale files in the resulting dist or strange and confusing errors. Avoid having them around.

And then you can build the `sdist`, and if possible, the `bdist_wheel` too:

```bash
python3 setup.py clean --all sdist bdist_wheel
```

#### Publishing to PyPI

To make a release of the project on PyPI, assuming you got some distributions in `dist/`, the most simple usage is:

```bash
twine upload --skip-existing dist/*.whl dist/*.gz dist/*.zip
```

In ZSH you can use this to upload everything in `dist/` that ain't a linux-specific wheel (you may need `setopt extended_glob`):

```bash
twine upload --skip-existing dist/*.(whl|gz|zip)~dist/*linux*.whl
```
