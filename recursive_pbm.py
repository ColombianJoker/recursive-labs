#!/opt/local/bin/uv run
# /// script
# dependencies = []
# requires-python = ">=3.11"
# ///

# imports
import argparse
import sys
from pathlib import Path


# auxiliary fn
def matrix2pbm(matrix: list[list[int]], filename: str):
    """
    Saves a nested list matrix to a P1 PBM file.
    Native PBM P1: 0 = White, 1 = Black.
    """
    if not matrix:
        return

    height = len(matrix)
    width = len(matrix[0])

    file_path = Path(filename)
    if file_path.suffix.lower() != ".pbm":
        file_path = file_path.with_suffix(".pbm")

    # Header: P1 (Plain BitMap), Width, Height
    header = f"P1\n{width} {height}\n"

    # Since the matrix is already in native format (0/1),
    # we just join the integers as strings.
    lines = [" ".join(map(str, row)) for row in matrix]
    content = "\n".join(lines)

    try:
        file_path.write_text(header + content + "\n")
        print(f"Successfully created '{file_path}' ({width}x{height})")
    except Exception as e:
        print(f"An error occurred while saving: {e}")
        sys.exit(1)


def set_square(matrix: list[list[int]], color: str, x1: int, y1: int, x2: int, y2: int):
    """
    Sets the pixels in the range [x1, x2] and [y1, y2] (inclusive)
    to the target color bit.
    """
    color_map = {"white": 0, "w": 0, "black": 1, "b": 1}
    target_bit = color_map.get(color.lower())

    if target_bit is None:
        raise ValueError("Invalid color for flipping.")

    # Inclusive range processing
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            matrix[y][x] = target_bit


def create_pbm_matrix(color_choice: str, size: int, filename: str):
    # 1. Map Input Color to Native PBM bits
    # 0 is White, 1 is Black
    color_map = {"white": 0, "w": 0, "black": 1, "b": 1}

    fill_value = color_map.get(color_choice.lower())
    if fill_value is None:
        print(
            f"Error: Invalid color '{color_choice}'. Use 'black', 'white', 'b', or 'w'."
        )
        sys.exit(1)

    # 2. Initialize the in-memory matrix with the native bit
    matrix = [[fill_value for _ in range(size)] for _ in range(size)]

    # 3. Save to file
    matrix2pbm(matrix, filename)


# main program
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a solid color PBM image.")

    # Positional or optional arguments - let's go with required named arguments for clarity
    parser.add_argument("color", help="Background color: 'black', 'white', 'b', or 'w'")
    parser.add_argument("size", type=int, help="Size of the square image (pixels)")
    parser.add_argument("filename", help="Name of the output file")

    args = parser.parse_args()

    create_pbm_matrix(args.color, args.size, args.filename)
