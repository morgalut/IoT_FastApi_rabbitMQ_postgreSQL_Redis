import base64
from PIL import Image

def compress_image(input_path, output_path, quality=20):
    """
    Compress an image to reduce file size.
    
    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the compressed image.
        quality (int): Compression quality (1-100, lower is more compressed).
    """
    img = Image.open(input_path)
    img.save(output_path, optimize=True, quality=quality)

def encode_image_to_base64(image_path, char_limit=None):
    """
    Encode an image file to a Base64 string.
    
    Args:
        image_path (str): Path to the image file.
        char_limit (int): Optional limit for the number of Base64 characters.
    
    Returns:
        str: Base64 encoded string.
    """
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode("utf-8")
        if char_limit:
            return base64_string[:char_limit]
        return base64_string

if __name__ == "__main__":
    image_path = input("Enter the path to the image: ")
    compressed_path = "compressed_image.jpg"

    # Step 1: Compress the image
    compress_image(image_path, compressed_path, quality=20)
    
    # Step 2: Encode to Base64 with character limit for command-line use
    char_limit = 1000  # Limit the string to 1000 characters
    base64_string = encode_image_to_base64(compressed_path, char_limit=char_limit)

    # Step 3: Save the output to a text file
    output_file = "encoded_image.txt"
    with open(output_file, "w") as file:
        file.write(base64_string)

    print(f"Compressed and limited Base64 string saved to {output_file}")
    print("Base64 Encoded String (for command-line use):")
    print(base64_string)
