# Codebox - CLI for Saving and Sharing Code Snippets

Codebox is a command-line interface (CLI) program that allows you to easily save and share code snippets directly from your terminal. It provides a simple and efficient way to manage your code snippets with features like adding, listing, and deleting snippets.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Adding a Snippet](#adding-a-snippet)
  - [Listing Snippets](#listing-snippets)
  - [Deleting Snippets](#deleting-snippets)
- [License](#license)

## Installation

To use Codebox, you need to have Python installed on your system. You can install Codebox using pip:

```bash
pip install --editable .
```

## Usage
### Adding a Snippet
To add a code snippet, use the following command:

```bash
codebox add --name <snippet_name> --tags <tag1> <tag2> ...
```

### Listing Snippets
To list all saved snippets, use the following command:

```bash
codebox list
```

### Deleting Snippets
To delete one or more snippets, use the following command:

```bash
codebox delete <snippet_id> ...
```

## License

Distributed under the MIT License. See `LICENSE` for more information.
