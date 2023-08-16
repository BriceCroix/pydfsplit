from dataclasses import dataclass
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from argparse import ArgumentParser
import sys
import os


def get_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog='pydfplit',
        description='Minimal software to split or merge pdf files.',
        epilog='')
    parser.add_argument('file', action='store',
                        help='File to be splitted or merged with another.')
    parser.add_argument('-o', '--output', action='store',
                        required=False, help='Output file name when merging files.', default='out.pdf')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--append', action='store',
                       help='File to be appended after first file.')
    group.add_argument('-s', '--split', action='store',
                       help='Index of page where to split input file.', type=int)

    return parser


@dataclass
class Args:
    """Main script arguments."""
    file: str  # Input file
    split: int  # Index at which to split input file
    appendix: str  # File to append at the end of input file
    output: str  # Output file


def process(args: Args):
    # Create output directory if missing
    dir = os.path.dirname(args.output)
    if (dir != ''):
        os.makedirs(dir, exist_ok=True)

    # Open first file
    reader = PdfReader(args.file)

    # args.appendix and args.split are mutually exclusive

    # If user wants to merge two files
    if (args.appendix is not None):
        reader_appendix = PdfReader(args.appendix)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        for page in reader_appendix.pages:
            writer.add_page(page)
        with Path(args.output).open(mode="wb") as f:
            writer.write(f)
    # If user wants to split file in two files
    else:
        if (args.split >= len(reader.pages) or args.split < 1):
            return
        output_without_ext, output_ext = os.path.splitext(args.file)
        writer = PdfWriter()
        for page in reader.pages[:args.split]:
            writer.add_page(page)
        output = output_without_ext + f'.0-{args.split-1}' + output_ext
        with Path(output).open(mode="wb") as f:
            writer.write(f)

        writer = PdfWriter()
        for page in reader.pages[args.split:]:
            writer.add_page(page)
        output = output_without_ext + \
            f'.{args.split}-{len(reader.pages)-1}' + output_ext
        with Path(output).open(mode="wb") as f:
            writer.write(f)


def main():
    parser = get_arg_parser()
    if (len(sys.argv) < 2 or (len(sys.argv) == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'))):
        parser.print_help()
        return
    parsed_args = parser.parse_args()
    args = Args(parsed_args.file, parsed_args.split,
                parsed_args.appendix, parsed_args.output)
    process(args)


if __name__ == "__main__":
    main()
