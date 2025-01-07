# spreadsheet

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

5. Run the application

```
python src/simple_spreadsheet/main.py
```

6. Run the tests

```
cd tests/automatic_grader
PYTHONPATH=$PYTHONPATH:.:../../../spreadsheet python markerrun/TestsRunner.py
```

### Useful commands

Once everything is set up, these one-liners can be used to run the application and the tests respectively.

```
source venv/bin/activate && python src/simple_spreadsheet/main.py
```

```
source venv/bin/activate && cd tests/automatic_grader && PYTHONPATH=$PYTHONPATH:.:../../../spreadsheet python markerrun/TestsRunner.py
```
