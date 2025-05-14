# Development Guide

## Setup

### Docker Installation

- **Windows:** [Docker Installation Guide](https://docs.docker.com/desktop/setup/install/windows-install/)  
- **Linux:** [Docker Installation Guide](https://docs.docker.com/desktop/setup/install/linux/)  

### Setting Up Environment Variables

Create a `.env` file in the root directory of the project and define the required environment variables.

## Run the app

```bash
docker compose up --build
```

## Run the application in the background

```bash
docker compose up --build -d 
```

## Stop the application

```bash
docker compose down
```

## Auto-Rebuilding Your Container on Code Changes

To automatically rebuild your container when you modify the source code, follow these steps:

1. First, start your container with:
   ```bash
   docker compose up --build
   ```

2. Then, in a separate terminal, run:
   ```bash
   docker compose watch
   ```

This will monitor your project for changes and automatically rebuild the container when necessary.

## Making changes in DB

1. First, install all dependencies locally:
   ```bash
   pip install -r requirements.txt
   ```

2. In another terminal run:
   ```bash
   docker compose up postgresql
   ```

3. In your .env change:
   ```bash
   DASHBOARDOP_ENV=local
   ```

3. Write your change message:
   ```bash
   flask db migrate -m "Adicionando coluna de cpf em alvo." # exemplo
   ```

4. Then you can apply the changes described by the migration script to your database:
   ```bash
   flask db upgrade
   ```

> **Note:** Each time the database models change, repeat the migrate and upgrade commands.

## Enter in a virtual enviroment

### For Bash/Zsh (Linux/macOS):

```bash
source app/.venv/bin/activate
```

### For Windows (Command Prompt):

```bash
app\.venv\Scripts\activate
```

### For Windows (PowerShell):

```bash
app\.venv\Scripts\Activate.ps1
```

> **Note:** If you're using VS Code, you need to select your virtual environment as the Python interpreter.  
> Follow this guide to set it up: [VS Code - Python Environments](https://code.visualstudio.com/docs/python/environments)

# Python PEP 8 Best Practices

PEP 8 is the official style guide for Python code. Following PEP 8 ensures code consistency, readability, and maintainability. Below are the key best practices extracted from PEP 8.

## 1. Code Layout

### 1.1 Indentation
- Use **4 spaces per indentation level**.

```python
if condition:
    do_something()
```

### 1.2 Line Length
- Limit all lines to **79 characters**.
- Limit docstrings and comments to **72 characters**.

```python
# This is a comment that is less than 72 characters long.
```

### 1.3 Blank Lines
- Use **two blank lines** to separate top-level functions and classes.
- Use **one blank line** inside functions to separate logic sections.

```python
def first_function():
    pass


def second_function():
    pass
```

## 2. Imports
- Always **import one module per line**.
- Use **absolute imports** whenever possible.
- Imports should be grouped in the following order:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports

```python
import os
import sys

import numpy as np

from mymodule import my_function
```

## 3. Naming Conventions
### 3.1 Variables and Functions
- Use **lowercase_with_underscores** for variable and function names.

```python
def calculate_total():
    total_amount = 100
    return total_amount
```

### 3.2 Constants
- Use **ALL_CAPS_WITH_UNDERSCORES** for constants.

```python
MAX_RETRIES = 5
```

### 3.3 Classes
- Use **CamelCase** for class names.

```python
class DataProcessor:
    pass
```

## 4. String Quotes
- Use **single (' ') or double (" ") quotes consistently**.
- Triple double-quotes (`"""`) for multi-line docstrings.

```python
name = "John"
message = 'Hello, world!'
```

## 5. Whitespace Usage
### 5.1 Around Operators
- Use **spaces around operators**.

```python
x = 10 + 5
```

### 5.2 Inside Brackets
- Avoid **extra spaces** inside parentheses, brackets, or braces.

```python
my_list = [1, 2, 3]
```

## 6. Docstrings and Comments
### 6.1 Docstrings
- Use triple double-quotes (`"""`) for docstrings.

```python
def add_numbers(a, b):
    """Return the sum of two numbers."""
    return a + b
```

### 6.2 Comments
- Write meaningful and concise comments.
- Use **#** for inline comments.

```python
# This function calculates the square of a number
def square(num):
    return num ** 2  # Exponentiation
```

## 7. Avoiding Common Pitfalls
- **Don't use mutable default arguments**.

```python
def append_to_list(item, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(item)
    return my_list
```

- **Use `is` for `None` comparisons**.

```python
if my_var is None:
    pass
```

## 8. Conclusion
Following PEP 8 ensures your code is readable, maintainable, and consistent with Python community standards. Use linters like `flake8` or `black` to enforce these best practices.