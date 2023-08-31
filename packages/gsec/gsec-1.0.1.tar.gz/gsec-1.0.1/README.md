# Git-Secret

## Requirements

- git
- [github-cli](https://cli.github.com/)
- `SECRET_KEY` environment variable or `.key` file in the root of the repository
> You can generate a secret key automatically by leaving the `SECRET_KEY` environment variable empty. It will be stored in the `.key` file.

## Installation

### Pip

```bash
pip install gsec
```

### From source

```bash
git clone 
cd git-secret
pip install -r requirements.txt
python src/main.py --help
```

## Usage

```bash
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add     Add a new secret
  delete  Delete a secret by ID
  edit    Edit a secret by ID
  list    List all secrets
  show    Show a secret by ID
```

## TODO

- [x] Add configuration file (json)
	- [x] Change repo path
	- [ ] ~Change secret key~
- [ ] Create packages
  - [x] PyPI
  - [ ] AUR
  - [ ] COPR
- [ ] Add tests
- [ ] Change the way `show` displays the secrets