from dataclasses import dataclass
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from argparse import ArgumentParser
import sys
import os
import customtkinter as ctk

def get_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog='pydfplit',
        description='Minimal software to split or merge pdf files.',
        epilog='Calling this without any argument will start the UI.')
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
    # Open first file
    reader = PdfReader(args.file)

    # args.appendix and args.split are mutually exclusive

    # If user wants to merge two files
    if (args.appendix is not None):
        # Create output directory if missing
        dir = os.path.dirname(args.output)
        if (dir != ''):
            os.makedirs(dir, exist_ok=True)

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

####################################################################################################

PAD : int = 10
PDF_EXT : str = ".pdf"

class PydfSplitUI(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        self.geometry("480x360")
        self.title('pydfsplit')

        self.tab_view = ctk.CTkTabview(self)
        self.split_tab = self.tab_view.add("Split")
        self.merge_tab = self.tab_view.add("Merge")
        self.tab_view.pack(fill='both')

        self._build_split_tab()
        self._build_merge_tab()

    def _build_split_tab(self):
        self.split_input_file = ctk.StringVar(self)
        self.split_index_str = ctk.IntVar(self, 1)

        self.split_input_frm = ctk.CTkFrame(self.split_tab)
        self.split_input_frm.pack(side=ctk.TOP, fill='x', pady=PAD)
        self.split_input_lbl = ctk.CTkLabel(self.split_input_frm, text="Input file")
        self.split_input_lbl.pack(side=ctk.LEFT)
        self.split_input_btn = ctk.CTkButton(self.split_input_frm, text="Browse", command=self.on_split_input_browse_pressed)
        self.split_input_btn.pack(side=ctk.RIGHT, padx=PAD)
        self.split_input_entry = ctk.CTkEntry(
            self.split_input_frm, textvariable=self.split_input_file)
        self.split_input_entry.pack(fill='x', expand=True, padx=PAD)

        self.split_index_frm = ctk.CTkFrame(self.split_tab)
        self.split_index_frm.pack(side=ctk.TOP, fill='x', pady=PAD)
        self.split_index_lbl = ctk.CTkLabel(
            self.split_index_frm, text="Split at page index")
        self.split_index_lbl.pack(side=ctk.LEFT)
        self.split_index_entry = ctk.CTkEntry(
            self.split_index_frm, textvariable=self.split_index_str)
        self.split_index_entry.pack(side=ctk.RIGHT, fill='x', expand=True, padx=PAD)

        self.split_validate_button = ctk.CTkButton(
            self.split_tab, text="Split !", command=self.on_split_pressed) 
        self.split_validate_button.pack(padx=PAD, pady=PAD)

    def _build_merge_tab(self):
        self.merge_input_file = ctk.StringVar(self)
        self.merge_append_file = ctk.StringVar(self)
        self.merge_output_file = ctk.StringVar(self, 'out.pdf')

        self.merge_input_frm = ctk.CTkFrame(self.merge_tab)
        self.merge_input_frm.pack(side=ctk.TOP, fill='x', pady=PAD)
        self.merge_input_lbl = ctk.CTkLabel(self.merge_input_frm, text="First input file")
        self.merge_input_lbl.pack(side=ctk.LEFT)
        self.merge_input_btn = ctk.CTkButton(self.merge_input_frm, text="Browse", command=self.on_merge_input_browse_pressed)
        self.merge_input_btn.pack(side=ctk.RIGHT, padx=PAD)
        self.merge_input_entry = ctk.CTkEntry(
            self.merge_input_frm, textvariable=self.merge_input_file)
        self.merge_input_entry.pack(fill='x', expand=True, padx=PAD)

        self.merge_append_frm = ctk.CTkFrame(self.merge_tab)
        self.merge_append_frm.pack(side=ctk.TOP, fill='x', pady=PAD)
        self.merge_append_lbl = ctk.CTkLabel(self.merge_append_frm, text="Second input file")
        self.merge_append_lbl.pack(side=ctk.LEFT)
        self.merge_append_btn = ctk.CTkButton(self.merge_append_frm, text="Browse", command=self.on_merge_append_browse_pressed)
        self.merge_append_btn.pack(side=ctk.RIGHT, padx=PAD)
        self.merge_append_entry = ctk.CTkEntry(
            self.merge_append_frm, textvariable=self.merge_append_file)
        self.merge_append_entry.pack(fill='x', expand=True, padx=PAD)

        self.merge_output_frm = ctk.CTkFrame(self.merge_tab)
        self.merge_output_frm.pack(side=ctk.TOP, fill='x', pady=PAD)
        self.merge_output_lbl = ctk.CTkLabel(self.merge_output_frm, text="Output file")
        self.merge_output_lbl.pack(side=ctk.LEFT)
        self.merge_output_btn = ctk.CTkButton(self.merge_output_frm, text="Browse", command=self.on_merge_output_browse_pressed)
        self.merge_output_btn.pack(side=ctk.RIGHT, padx=PAD)
        self.merge_output_entry = ctk.CTkEntry(
            self.merge_output_frm, textvariable=self.merge_output_file)
        self.merge_output_entry.pack(fill='x', expand=True, padx=PAD)

        self.merge_validate_button = ctk.CTkButton(
            self.merge_tab, text="Merge !", command=self.on_merge_pressed) 
        self.merge_validate_button.pack(padx=PAD, pady=PAD)

    def on_split_input_browse_pressed(self):
        self.split_input_file.set(ctk.filedialog.askopenfilename(filetypes=[("Portable Document Format Files", PDF_EXT)]))

    def on_split_pressed(self):
        self.configure(state=ctk.DISABLED)
        try:
            process(Args(self.split_input_file.get(), self.split_index_str.get(), None, None))
        except Exception as e:
            print(e, file=sys.stderr)
        self.configure(state=ctk.NORMAL)

    def on_merge_input_browse_pressed(self):
        self.merge_input_file.set(ctk.filedialog.askopenfilename(filetypes=[("Portable Document Format Files", PDF_EXT)]))

    def on_merge_append_browse_pressed(self):
        self.merge_append_file.set(ctk.filedialog.askopenfilename(filetypes=[("Portable Document Format Files", PDF_EXT)]))

    def on_merge_output_browse_pressed(self):
        self.merge_output_file.set(ctk.filedialog.asksaveasfilename(filetypes=[("Portable Document Format Files", PDF_EXT)], defaultextension=PDF_EXT))

    def on_merge_pressed(self):
        self.configure(state=ctk.DISABLED)
        try:
            process(Args(self.merge_input_file.get(), None, self.merge_append_file.get(), self.merge_output_file.get()))
        except Exception as e:
            print(e, file=sys.stderr)
        self.configure(state=ctk.NORMAL)


####################################################################################################


def main():
    if (len(sys.argv) < 2):
        app = PydfSplitUI()
        app.mainloop()
    else:
        try:
            parser = get_arg_parser()
            if (len(sys.argv) < 2 or (len(sys.argv) == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'))):
                parser.print_help()
                return
            parsed_args = parser.parse_args()
            args = Args(parsed_args.file, parsed_args.split,
                        parsed_args.appendix, parsed_args.output)
            process(args)
        except Exception as e:
            print(e, file=sys.stderr)


if __name__ == "__main__":
    main()
