#!/usr/bin/env python3
"""
rotate_pdf.py

A simple command‑line utility that rotates pages of a PDF file by a
specified angle.

Usage:
    python rotate_pdf.py -i INPUT.pdf -o OUTPUT.pdf --angle 90

Supported options:
    -i, --input     Path to the input PDF file.
    -o, --output    Path where the rotated PDF will be written.
    -a, --angle     Rotation angle in degrees. Must be one of
                    90, 180, 270 (counter‑clockwise).

The script uses PyPDF2 to perform the rotation.
"""

import argparse
import sys
import os
from pathlib import Path

try:
    # PyPDF2 >= 3.0 uses PdfReader / PdfWriter
    from PyPDF2 import PdfReader, PdfWriter
except ImportError as exc:
    print("Error: PyPDF2 is not installed. Install it via pip:")
    print("    pip install PyPDF2")
    sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command‑line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Rotate PDF pages by a specified angle."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to the input PDF file."
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Path to write the rotated PDF file."
    )
    parser.add_argument(
        "-a", "--angle",
        type=int,
        required=True,
        choices=[90, 180, 270],
        help="Rotation angle (90, 180, or 270 degrees)."
    )
    return parser.parse_args()


def rotate_pdf(input_path: Path, output_path: Path, angle: int) -> None:
    """
    Rotate every page of the input PDF by the given angle and write
    the result to the output file.

    Args:
        input_path (Path): Path to the source PDF.
        output_path (Path): Path to write the rotated PDF.
        angle (int): Angle in degrees (90, 180, or 270).
    """
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {input_path}")

    # Read the source PDF
    reader = PdfReader(str(input_path))
    writer = PdfWriter()

    # Rotate each page
    for page in reader.pages:
        page.rotate(page.get("/Rotate") + angle if page.get("/Rotate") else angle)
        writer.add_page(page)

    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the rotated PDF
    with open(output_path, "wb") as f_out:
        writer.write(f_out)


def main() -> None:
    args = parse_arguments()

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    try:
        rotate_pdf(input_path, output_path, args.angle)
    except Exception as exc:
        print(f"Error while rotating PDF: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Rotated PDF written to: {output_path}")


if __name__ == "__main__":
    main()
