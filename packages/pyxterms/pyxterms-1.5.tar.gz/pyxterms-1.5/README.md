# Pyxterms - Terminal Enhancement Library

[![GitHub](https://img.shields.io/badge/GitHub-lutherantz-blue)](https://github.com/lutherantz)
[![Version](https://img.shields.io/badge/Version-1.0-green)](https://github.com/lutherantz/pyxtemr/releases/tag/v1.0)
[![License](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/licenses/MIT)

Pyxterms is a Python library designed to enhance terminal interactions by providing useful utilities for terminal manipulation, cursor control, color formatting, animations, and text centering.

## Features

- Clear the terminal screen
- Set terminal title
- Execute system commands
- Get terminal size
- Hide and show the terminal cursor
- Apply custom colors and gradients
- Create typewriter text animations
- Center text both horizontally and vertically

## Installation

You can install Pyxtemr using pip:

	pip install pyxtemr` 

## Usage

Import the module and explore its capabilities:

```python
from pyxtemr import Term, Cursor, Color, Anim, Center

# Clear the terminal
Term.clear()

# Set terminal title
Term.title("My Awesome Terminal App")

# Hide the cursor
Cursor.hide_cursor()

# Apply custom colors
print(Color.red + "This text is red" + Color.reset)

# Create a typewriter animation
Anim.typing("Hello, world!", slp=0.1)

# Center text both horizontally and vertically
centered_text = Center.center("Centered Text")
print(centered_text)` 
```

## Documentation

For detailed information about the available functions and their usage, please refer to the [documentation](https://github.com/lutherantz/pyxtemr/blob/main/docs.md).

## Contributing

Contributions are welcome! Feel free to open issues or pull requests on the [GitHub repository](https://github.com/lutherantz/pyxtemr).

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/lutherantz/pyxterms/blob/main/LICENSE) file for details.