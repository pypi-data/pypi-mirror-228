# indoquake
A Latest Earthquake Detection Package Taken Based on BMKG | Meteorological, Climatological, and Geophysical Agency
> This package was made using the beautifulsoup4 and request packages
> 
> The data is also taken from the [BMKG](https://www.bmkg.go.id/ "earthquake data website")

# requiretment package
> beautifulsoup4
> requests

# Author
> Danang Firmanto

# How to use

```python
from src.quake import ekstrasi_data, tampilkan_data

if __name__ == '__main__':
    print('Earthquake data from BMKG')
    result = ekstrasi_data()
    tampilkan_data(result)
```


