<!-- GETTING STARTED -->
## Getting Started

### Clone Repo
* Clone library repo
  ```sh
  git clone https://github.com/bot-auto/botdata-sdk.git
  cd botdata-sdk
  ```

### Venv
* Create virtual environment
  ```sh
  python3 -m venv venv
  source venv/bin/activate
  ```

### Install
* Run setup
  ```sh
  pip3 install .
  ```

### Pre-commit
* Get pre-commit register
  ```sh
  pre-commit install # install .pre-commit-config.yaml, automatic git commit check
  pre-commit run --all-files
  ```

### Release
* Update version
  Update version in pyproject.toml `version = "<new version>"`
* Run setup
  ```sh
  python3 setup.py sdist bdist_wheel # build dist and wheel
  twine upload dist/*   # upload to pypi
  ```