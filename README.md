# simple_spreadsheet

`simple_spreadsheet` is a simple terminal-based application that allows users to create and edit spreadsheets. It is coded in Python and has support for:

- Creating spreadsheets
- Editing cells, with support for texts, numbers, and formulas.
- Creating complex formulas with support for:
  - Numbers and cell references (e.g. `A1`, `B2`, `3.14`)
  - Basic arithmetic operators (`+`, `-`, `*`, `/`)
  - Parentheses
  - Basic functions (`SUMA`, `PROMEDIO`, `MAX`, `MIN`), that can take as arguments:
    - Cell references (e.g. `SUMA(A1;B20)`)
    - Numbers (e.g. `SUMA(1;2)`)
    - Cell ranges (e.g. `SUMA(A1:A3)`)
    - And nested functions
- Displaying the spreadsheet, with automatic update of formulas as dependent cells change.
- Saving a spreadsheet to a `.s2v` file
- Loading a spreadsheet from a `.s2v` file

<img width="1162" alt="App screenshot" src="https://github.com/user-attachments/assets/c90391c9-328f-498a-8e56-c3365b396b96" />

## Important notes

- We have implemented 2 controllers, one specifically for the checker, and one that includes the UI and has no dependencies on the checker and hence, is easy to distribute as a package.

- The project has been developed using Visual Studio Code. We are available for a live demo/correction if needed. Just email us!

- In terms of architecutre, since the consultation, we have:
  - implemented all the inheritance suggestions, those large nested if-else chains have been replaced by polymorphism.
  - implemented the visitor design pattern for the formula evaluation, removing type enums and the need for type checking.

## How to run locally

### Prepare the environment

1. Clone the repository and navigate to the project directory
2. Create a virtual environment

```
python3 -m venv venv
```

3. Activate the virtual environment

```
source venv/bin/activate
```

4. Install the dependencies

```
pip install -r requirements.txt
```

5. Install as a package

```
pip install -e .
```

6. Run the application

```
python src/simple_spreadsheet/main.py
```

7. Run the tests

```
cd tests/automatic_grader
PYTHONPATH=$PYTHONPATH:../../../spreadsheet python markerrun/TestsRunner.py
```

<strong>Note:</strong> This instruction assumes that you have Python 3 installed on your machine and that you are using a Unix-like operating system. If you are using Windows, the commands may be slightly different.

### Useful commands

Once everything is set up, these one-liners can be used to run the application and the tests respectively.

```
source venv/bin/activate && python src/simple_spreadsheet/main.py
```

```
source venv/bin/activate && cd tests/automatic_grader && PYTHONPATH=$PYTHONPATH:../../../spreadsheet python markerrun/TestsRunner.py
```
