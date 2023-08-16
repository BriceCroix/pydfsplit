# pydfsplit

`pydfsplit` is a minimalist tool to split or merge pdf files.

## Examples

- Split a pdf file in two files (pages 0 and 1 in one file, pages 2, 3 and so on in another):
```shell
pydfplit --split 2 "my_file.pdf"
```

- Merge two pdf files
```shell
pydfplit --append "second_file" --output "my_output.pdf" "first_file.pdf"
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