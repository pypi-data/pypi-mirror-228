# Si Feng

Si Feng (思风) is a quant research framework built by our team, SiFeng. It is mainly desinged only to be used within our team but also welcome public useres. Feel free to tell us what features you want to add to this project.

## How to use

The project is posted on [github](https://github.com/zty200489/sifeng). To use this python package, simple use install it from [PyPI](https://pypi.org/project/sifeng/) to your local environment with:

```console
pip install sifeng
```

## Features

### Version 0.1.6

- (Bug fix) Swapped processing sequence. Parsing data annually avoids running into forced-aborted connections.
- Ignored index when concating pandas dataframes.

### Version 0.1.5

- Added partitioned table support. Slicing up requests into year-specific subrequests, speeding up the search.

### Version 0.1.4

- Thread pooling fetchers based on grequests.
- kline and indicators updated every day.

