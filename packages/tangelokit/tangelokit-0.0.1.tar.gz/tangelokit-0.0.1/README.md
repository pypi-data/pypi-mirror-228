# tangelo-data-kit

Small lib using for tangelo to build information
Developed by Arnold Blandon 2023

## Examples of How To Use

Generating Completed data Stracture

```python
from tangelokit import GenerateDataStructure
process = GenerateDataStructure(
    credit_lines = [],
    disbursements = [],
    products = [],
    clients = []
)

```

Validate error_messages empty before build information:

```python
process.error_messages
```

processed data:

```python
process.build_information()
```

GET all data:

```python
process.get_all_data_processed()
```

filter data by params: client, credit_line, disbursement:

```python
process.filter_data(params)
```
# pip install wheel  # install whell
# pip install setuptools_rust
# pip install --upgrade pip setuptools
# pip install twine  # install twine

# python3 setup.py sdist bdist_wheel # build package
#twine upload dist/*