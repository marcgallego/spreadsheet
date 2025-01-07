# spreadsheet

## How to run locally

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
