# qsmap Package

The qsvin package provides functionality for decoding VINs. Use of the package is supported both Databricks and locally. Be sure you have valid credentials for using package locally. Package returns **pandas DataFrame**. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install qsvin.

```bash
pip install qsvin
```

## Usage

Here are some examples of how to use QVIN package:

### Decode Vin
```python
from qsvin import QVIN

vd = QVin()

vd.lookup_vin(vin='VF1LM1B0H36666155')
```

### Decode Vin from local machine
```python
from qsvin import QVIN

credentials={
    "server_hostname": "********",
    "http_path": "********",
    "access_token": "********"
}
vd = QVin(credentials)

vd.lookup_vin(vin='VF1LM1B0H36666155')
```

### Decode VINs
```python
from qsvin import QVIN

vd = QVin()

vd.lookup_vin(vin=['VF1LM1B0H36666155', '1M8GDM9AXKP042788'])
```

### Decode VINs + additional features useful for ML 
```python
from qsvin import QVIN

vd = QVin()

vd.lookup_vin(vin=['VF1LM1B0H36666155', '1M8GDM9AXKP042788'], feature=True)

vd.get_distinct() # get all distinct values for features (body_type, fuel_type)
```

### Decode VIN hierarchicallly (match either on wms or vis or vds)
```python
from qsvin import QVIN

vd = QVin()

vd.lookup_vin(vin='1M8LM1B0HKP042788', hierarchical=True)
```

### Hive Query
```python
from qsvin import QVIN

vd = QVin()

vd.lookup_vin(vin=None, query="vds == '6B9T2' or vds == 'LM1B0H'")
```

### Export excel file
```python
from qsvin import QVIN

vd = QVin()

vd.export_excel(vin=['VF1LM1B0H36666155', '1M8GDM9AXKP042788'], fname="output.xlsx")
```

### Import new data with backuping old version
```python
from qsvin import QVIN

vd = QVin()

new_fake_data =vd.lookup_vin(vin='1M8LM1B0HKP042788', hierarchical=True)
new_fake_data.loc[0, 'year']=2023
new_fake_data.loc[0,'source']="yaroslav"
new_fake_data.loc[1,'year']=2022
new_fake_data.loc[1,'source']="yaroslav again"

vd.update_db(new_fake_data) # so if the same key (wmi, vis, vds) is found, the old version moved to backupDB, new row is inserted to main one
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)