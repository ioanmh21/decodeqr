# QR Code Decoder

This project provides a Python implementation for decoding QR codes. It can read a QR code image (PNG format), extract its binary data, apply the necessary unmasking, and then decode the embedded information such as the encoding mode and the actual message. 

## Files

- `decode.py`: The main script that orchestrates the QR code decoding process. It handles image loading, preprocessing, and calling the decoding functions.
- `decode_functions.py`: Contains various helper functions for extracting format information, determining mask patterns and error correction levels, and decoding the data bits based on the encoding mode.
- `masks.py`: Defines the different mask patterns used in QR codes and functions to apply and correct these masks. It also includes functions to identify and exclude fixed patterns (finder patterns, alignment patterns, timing patterns, etc.) from the data area.
- `qrcode.png`: An example QR code image used as input for the `decode.py` script. (This file is expected to be in the same directory as `decode.py`.)

## Features

-   **PNG to Binary Matrix Conversion**: Converts a QR code PNG image into a binary matrix representation. 
-   **Debordare (Cropping)**: Automatically crops the QR code image to remove any surrounding whitespace. 
-   **Format Information Extraction**: Extracts the format information bits from the QR code, which contain details about the mask pattern and error correction level. 
-   **Mask Pattern Detection and Unmasking**: Identifies the mask pattern applied to the QR code and unmasks the data region to reveal the original data bits. 
-   **Data Bit Extraction**: Extracts the raw data bits from the unmasked QR code matrix. 
-   **Encoding Mode Detection**: Determines the encoding mode (Numeric, Alphanumeric, Byte, Kanji) of the QR code data. 
-   **Character Count Extraction**: Reads the character count indicator for the respective encoding mode. 
-   **Data Decoding**: Decodes the extracted data bits into a human-readable string based on the detected encoding mode. 
-   **Visualization**: (Commented out in `decode.py` but can be enabled) Provides a `display` function to visualize the binary matrix representation of the QR code. (This is a potential feature, currently commented out)

## How to Run 

1.  **Ensure you have the necessary libraries installed**:
    ```bash
    pip install numpy Pillow
    ```
2.  **Place your QR code image**: Make sure `qrcode.png` (or your desired QR code image renamed to `qrcode.png`) is in the same directory as `decode.py`.
3.  **Run the main script**:
    ```bash
    python decode.py
    ```

The decoded data will be printed to the console. 

## Code Structure and Logic 

### `decode.py`

-   `png_to_binary_matrix(file_path, target_size=29)`:
    -   Opens a PNG image, converts it to grayscale, resizes it to `target_size`x`target_size`, and converts pixels to 0s and 1s (black/white).
    -   Returns a list of lists representing the binary matrix.
-   `display(mat)`: (Currently commented out)
    -   Takes a binary matrix and scales it up for better visualization, then displays it as an image.
-   `debordare(mat)`:
    -   Iteratively removes rows and columns of zeros from the border of the matrix until a non-zero pixel is encountered, effectively cropping the QR code.
-   **Main execution flow**:
    -   Loads `qrcode.png` using `png_to_binary_matrix`.
    -   Calls `debordare` to crop the matrix.
    -   Converts the matrix to a NumPy array.
    -   Uses `masks.get_data_matrix` to get a matrix indicating data areas.
    -   Extracts `format_info` using `df.extract_format_information`.
    -   Derives `mask_pattern`, `error_correction_level`, and `error_correction_bits` from `format_info`.
    -   Unmasks the QR code matrix using `masks.mask` and `masks.correct_mask`.
    -   Extrăge `data_bits` from the unmasked matrix using `df.extract_data_bits`.
    -   Determines the `mode` and `count` of characters.
    -   Finally, `df.extract_data` decodes the bits into the final string, which is then printed.

### `decode_functions.py`

-   `extract_format_information(matrix)`:
    -   Extracts the 15 bits of format information located in specific positions around the finder patterns.
-   `get_mask_pattern(format_info)`:
    -   Extracts the 3 bits representing the mask pattern from the format information.
-   `get_error_correction_level(format_info)`:
    -   Extracts the 2 bits representing the error correction level from the format information.
-   `get_error_correction_bits(format_info)`:
    -   Extracts the remaining error correction code bits from the format information.
-   `get_encoding_mode(data_bits)`:
    -   Determines the data encoding mode (Numeric, Alphanumeric, Byte, Kanji) based on the first 4 bits of the data stream.
-   `extract_data_bits(matrix)`:
    -   Implements the zigzag pattern reading logic to extract the actual data bits from the unmasked QR code matrix, skipping functional patterns.
-   `get_character_count(data_bits, mode)`:
    -   Reads the character count indicator from the data stream based on the detected encoding mode.
-   `extract_data(data_bits, mode, count)`:
    -   Decodes the raw data bits into a string according to the specified `mode` (Numeric, Byte, or Alphanumeric) and `count`.

### `masks.py`

-   `mask_condition`: A list of lambda functions, each representing one of the 8 possible mask patterns.
-   `get_alignment_positions(version)`:
    -   Calculates the coordinates for the alignment patterns based on the QR code version.
-   `get_data_matrix(mat)`:
    -   Creates a matrix of the same size as the QR code, marking all non-data areas (finder patterns, timing patterns, alignment patterns, format information areas, version information areas) as '1' and data areas as '0'. This helps in identifying where data bits are located.
-   `mask(index, mat)`:
    -   Applică the specified mask pattern (`index`) to the QR code matrix. It XORs the bits in the data areas of the matrix based on the mask condition.
-   `correct_mask(k)`:
    -   A utility function to map the mask pattern bits extracted from the format information to the correct mask function index.

## Limitations

-   This implementation currently supports decoding specific versions of QR codes (implied by the `target_size=29` in `png_to_binary_matrix` and the version calculation `((n - 21) // 4) + 1`).
-   Error correction is not explicitly performed on the data bits; the `error_correction_level` and `error_correction_bits` are extracted but not used for correcting errors in the data itself. This means if the QR code is damaged, it might not decode correctly.
-   Only Numeric, Alphanumeric, and Byte encoding modes are fully implemented for data extraction. Kanji mode is identified but not decoded.
