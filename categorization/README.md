Python code for bug categorization
==================================

We use custom Python classes to categorize the studied bugs,
as we find it more convenient and extensible.
You can find the full documentation at `docs` directory.
The bugs are saved in `{java,kotlin,groovy,scala}.py`.
Each file contains 4 lists, one list contains 20 bugs that compose one
iteration.
To serialize the bugs into two JSONs, one for the bugs and one for the
characteristics, you can use the following command.

```bash
python serialize.py bugs.json characteristics.json
```

The above command creates the files `bugs.json` and `characteristics.json`.
`bugs.json` contains the dataset of the 320 typing-related bugs and
`characteristics.json` contains the program characteristics of their test
cases.
