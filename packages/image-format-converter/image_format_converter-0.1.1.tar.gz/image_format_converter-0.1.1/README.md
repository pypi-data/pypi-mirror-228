# Image Format Converter

A lightweight Python package that converts images in a directory from one format to another while preserving their dimensions.

**Features:**
- Convert images from one format (e.g., JPEG) to another (e.g., PNG).
-  Option to save the converted images in a different directory.
-  Option for recursive conversion in subdirectories.
-  Option to overwrite the original images with the converted ones.

## Installation

To install the Image Format Converter, use pip:

```
pip install image-format-converter
```

## Usage

After installing the package, you can use it from the command line:

```
image-format-converter -d DIRECTORY -i INPUT_FORMAT -o OUTPUT_FORMAT [OPTIONS]
```
### Parameters

    -d, --directory: Path of the directory containing images to be converted.
    -i, --input_format: Input image format (e.g., jpeg, png).
    -o, --output_format: Output image format (e.g., png, bmp).
    -od, --output_directory: Directory to save the converted images. If not specified, images will be saved in the input directory.
    -r, --recursive: Use this flag to process files in subdirectories too.
    --overwrite: Use this flag to overwrite the original image with the converted one.

## Examples

#### Basic Conversion:

Convert all JPEG images in the `images/` directory to PNG.

```
image-format-converter -d images/ -i jpeg -o png
```

#### Saving to a Different Directory:

Convert all JPEG images in the `images/` directory to PNG and save them in `converted/` directory.

```
image-format-converter -d images/ -i jpeg -o png -od converted/
```

#### Recursive Conversion:

Convert all JPEG images in the `images/` directory and its subdirectories to PNG.

```
image-format-converter -d images/ -i jpeg -o png -r
```

#### Overwriting Original Images:

Convert all JPEG images in the `images/` directory to PNG and replace the original JPEGs.

```
image-format-converter -d images/ -i jpeg -o png --overwrite
```

## License

This project is open-source and available under the MIT License.

