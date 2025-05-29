# heatmetrics Python Package

This Python package provides functions to calculate the following heat metrics: (1) Wet-Bulb Globe Temperature (WBGT), (2) Universal Thermal Climate Index (UTCI), (3) Dewpoint Temperature, (4) Net Effective Temperature, and (5) Humidex. The WBGT function follows the Liljegren et al. (2008) approach. The WBGT function and functions therein were translated from the heatmetrics R package (2022) to Python.

This package is provided "as-is," with no warranty whatsoever.

# Installation
```
pip install -i https://test.pypi.org/simple/ heatmetrics-python==0.0.26
```

# Usage
```
from heatmetrics_python import wbgt

wbgt.wbgt(2020, 7, 4.5, 42.36, -71.06, 700, 0.5, 0.5, 1013, 30, 60, 2, 10, -0.052, 1)
```





