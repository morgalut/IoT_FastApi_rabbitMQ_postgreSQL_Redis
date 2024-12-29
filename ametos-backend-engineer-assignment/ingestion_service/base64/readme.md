
# Image Compression and Base64 Encoding

This module provides tools for compressing images and encoding them into Base64 format. This can be particularly useful for reducing the size of images before transmitting them over networks where bandwidth is a concern or embedding images directly into HTML or CSS files.

## Features

- **Compress Image**: Reduces the file size of images using a specified quality parameter.
- **Encode Image to Base64**: Converts images to a Base64-encoded string, optionally truncating to a character limit for easier handling in environments where long strings are problematic (e.g., command lines).

## Requirements

- Python 3.x
- Pillow library

## Installation

Before running the script, ensure you have the Pillow library installed, which can be done via pip:

```bash
pip install Pillow
```

## Usage

The script can be executed directly from the command line. Here is how you can use the script:

1. **Compress an Image**
   - Provide the path to the input image.
   - Specify the path for the output (compressed) image.
   - Set the desired quality of the compression (1-100).

2. **Encode the Image to Base64**
   - Specify the path to the image to be encoded.
   - Optionally, set a character limit for the Base64 output to ensure it doesn't exceed command-line input limits.

Example of running the script:

```bash
python encode_base64.py
```

You will be prompted to enter the path to the image file you wish to compress and encode. After processing, the Base64-encoded image string will be saved to a text file, and displayed in the console with a character limit for easier usage in command-line environments.

## Output

The script will generate:
- A compressed image file.
- A Base64 encoded string saved in a text file (`encoded_image.txt`).
- The same Base64 string output to the console, truncated according to the specified character limit.

This tool is designed to be simple to use for basic image processing tasks in development environments or small-scale applications. It is not intended for large-scale production use without further enhancements for error handling and performance optimization.


