import os
import math
import argparse
import logging
from PIL import Image, UnidentifiedImageError

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Terminal colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Image Formats Supported
ALLOWED_FORMATS = ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'webp', 'ico']


def determine_format_size_unit(size_in_bytes: int) -> str:
    """ Convert a size in bytes into the most suitable unit (bytes, KB, MB, GB, etc.) """

    if size_in_bytes == 0:
        return "0 bytes"

    size_names = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    i = int(math.floor(math.log(size_in_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_in_bytes / p, 2)

    return f"{s} {size_names[i]}"


def print_final_statistics(original_space: int, total_saved_space: int, total_files_converted: int) -> None:
    """ Formats and print the final statistics after converting all images. """

    # Total Change
    if total_saved_space > 0:
        color = GREEN
        total_text = 'Total space saved'
    else:
        color = RED
        total_text = 'Total space increased'

    # Total Percentage
    if original_space != 0:
        change_percent = (total_saved_space / original_space) * 100
    else:
        change_percent = 0

    # Average change
    avg_saved_space = total_saved_space / total_files_converted if total_files_converted else 0

    if avg_saved_space > 0:
        average_text = 'Saved on average'
    else:
        average_text = 'Increased on average'

    # Print statistics
    logger.info(
        f"{total_text}: {color} {determine_format_size_unit(abs(total_saved_space))} ({abs(change_percent):.2f}%){RESET}")
    logger.info(
        f"{average_text}: {color} {determine_format_size_unit(abs(avg_saved_space))} per file over {total_files_converted} files.{RESET} \n")


def set_image_output_mode(im: Image.Image, output_format: str) -> Image.Image:
    """ Sets the color output mode based on the target output format. """

    if output_format.lower() == 'jpeg' or output_format.lower() == 'jpg':
        # RGB mode for JPEG format
        if im.mode != 'RGB':
            im = im.convert('RGB')

    elif output_format.lower() == 'png':
        # RGBA mode for PNG format
        if im.mode != 'RGBA':
            im = im.convert('RGBA')

    elif output_format.lower() == 'gif':
        # Palette mode for GIF format
        if im.mode != 'P':
            im = im.convert('P')

    return im


def convert_images_in_directory(directory: str, input_format: str, output_format: str,
                                output_directory: str = None,
                                recursive: bool = False,
                                overwrite: bool = False) -> None:
    """
    Convert images in a given directory from one format to another.
    
    Extra options:
    - Saving converted images to a different output directory
    - Recursive conversion of images in subdirectories
    - Overwriting the original image with the converted one
    
    Parameters:
        directory (str): Path to the directory where the convertion should start.
        input_format (str): Format of images to be converted.
        output_format (str): Format for the images after conversion.
        output_directory (str, optional): Directory where the converted images should be saved.
        recursive (bool, optional): If True, will process files in subdirectories too.
        overwrite (bool, optional): If True, will replace original image with the converted one.
    """

    original_space = 0
    total_saved_space = 0
    total_files_converted = 0

    for root, dirs, files in os.walk(directory):

        if not recursive:
            del dirs[:]  # Removes subdirectories

        for file in files:
            if file.lower().endswith(input_format.lower()):
                input_file_path = os.path.join(root, file)

                if overwrite:
                    output_file_path = os.path.splitext(input_file_path)[0] + "." + output_format

                else:
                    relative_path = os.path.relpath(root, directory)
                    output_subdirectory = os.path.join(output_directory or directory, relative_path)
                    output_file_path = os.path.join(output_subdirectory, file[:-len(input_format)] + output_format)

                    # Create output path if needed
                    if output_subdirectory:
                        os.makedirs(output_subdirectory, exist_ok=True)

                try:
                    with Image.open(input_file_path) as im:

                        # Set the correct mode based on the output format
                        im = set_image_output_mode(im, output_format)

                        im.save(output_file_path)

                        original_size = os.path.getsize(input_file_path)
                        new_size = os.path.getsize(output_file_path)

                        # Removed the original files if needed
                        if overwrite and input_file_path != output_file_path:
                            os.remove(input_file_path)

                        # Calculate file space changes
                        original_space += original_size
                        saved_space = original_size - new_size
                        total_saved_space += saved_space
                        total_files_converted += 1
                        saved_percent = (saved_space / original_size) * 100

                        color = GREEN if saved_space > 0 else RED
                        sign = '-' if saved_space > 0 else '+'

                        conversion_info = (
                            f"Converted: {file} [{determine_format_size_unit(original_size)}] -> {output_format} "
                            f"[{determine_format_size_unit(new_size)}] "
                            f"{color}({sign}{abs(saved_percent):.2f}%) "
                            f"({sign}{determine_format_size_unit(abs(saved_space))}){RESET} \n"
                        )

                        logger.info(conversion_info)


                except UnidentifiedImageError:
                    logger.info(f"Failed to process {input_file_path}")

    print_final_statistics(original_space, total_saved_space, total_files_converted)


def main():
    parser = argparse.ArgumentParser(
        description="Convert image formats in a directory while preserving the image dimensions. Refer to the readme "
                    "for detailed examples.",
        add_help=True)
    parser.add_argument("-d", "--directory", type=str, required=True,
                        help="Path of the directory containing images to be converted.")
    parser.add_argument("-i", "--input_format", type=str, required=True, choices=ALLOWED_FORMATS,
                        help="Input image format (e.g., jpeg, png).")
    parser.add_argument("-o", "--output_format", type=str, required=True, choices=ALLOWED_FORMATS,
                        help="Output image format (e.g., png, bmp).")
    parser.add_argument("-od", "--output_directory", type=str,
                        help="Directory to save the converted images. If not specified, images will be saved in the "
                             "input directory.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Process files in subdirectories too.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite the original image with the converted one.")

    args = parser.parse_args()

    convert_images_in_directory(args.directory, args.input_format, args.output_format, args.output_directory,
                                args.recursive, args.overwrite)


if __name__ == "__main__":
    main()
