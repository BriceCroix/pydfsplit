# pydfsplit

`pydfsplit` is a minimalist tool to split or merge pdf files.

## Examples

- Split a pdf file in two files at page 2 (starting at page 0):
```shell
pydfplit --split 2 --output "my_output.pdf" "my_file.pdf"
```

- Merge two pdf files
```shell
pydfplit --appendix "second_file" --output "my_output.pdf" "first_file.pdf"
```

## About execution

The executable `pydfsplit` can be compiled from the file `pydfsplit.py` with [pyinstaller](https://pypi.org/project/pyinstaller/) :

```shell
pyinstaller -F pydfsplit.py 
```

You can alternatively directly run the python file :
```shell
python pydfsplit.py [...]
```