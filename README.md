# pydfsplit

`pydfsplit` is a minimalist tool to split or merge pdf files.

## Command-line examples

- Split a pdf file in two files (pages 0 and 1 in one file, pages 2, 3 and so on in another):
```shell
pydfplit --split 2 "my_file.pdf"
```

- Merge two pdf files
```shell
pydfplit --append "second_file" --output "my_output.pdf" "first_file.pdf"
```

- A simple UI is available as well when called without any arguments.

## About execution

Please use virtual environments when working on this project :

```shell
cd this/project/folder
python -m venv .
source bin/activate
```

The executable `pydfsplit` can be compiled from the file `pydfsplit.py` with [pyinstaller](https://pypi.org/project/pyinstaller/) :

```shell
cd this/project/folder
pyinstaller --clean --onefile --windowed pydfsplit.py --paths lib/python3.10/site-packages --add-data "lib/python3.10/site-packages/customtkinter:customtkinter"
```
Note that on Windows the path separator is `;`, not `:` as shown above in the `--add-data` option.

You can alternatively directly run the python file :
```shell
python pydfsplit.py [...]
```