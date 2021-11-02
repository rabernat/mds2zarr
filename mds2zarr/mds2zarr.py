from collections.abc import Mapping
import json
from typing import Tuple, List, Optional, Any

from pydantic import validator
from pydantic.dataclasses import dataclass

import numpy as np
import zarr

# https://github.com/numpy/numpy/issues/20236
# from numpy.typing import DTypeLike
DTypeLike = Any

class DataFileConfig:
    arbitrary_types_allowed = True

@dataclass(frozen=True, config=DataFileConfig)
class DataFile(Mapping):
    path: str
    shape: Tuple[int, ...]
    dtype: DTypeLike

    @validator('dtype')
    def valid_numpy_dtype(cls, v):
        return np.dtype(v)

    @property
    def ndim(self) -> int:
        return len(shape)

    def _zarray(self):
        return json.dumps({
            "chunks": list(self.shape),
            "compressor": None,
            "dtype": self.dtype.str,
            "fill_value": None,
            "filters": None,
            "order": "C",
            "shape": list(self.shape),
            "zarr_format": 2
        })

    def _zattrs(self):
        return json.dumps({
            'foo': 'bar'
        })

    def __getitem__(self, key):

        # TODO: replace with case in python 3.10

        if key==".zarray":
            return self._zarray()
        elif key==".zattrs":
            return self._zattrs()
        else:
            return self._chunk_reference_for(key)

    def __iter__(self):
        yield '.zarray'
        yield '.zattrs'
        yield '0.0'

    def __contains__(self, item) -> bool:
        if item=='.zarray':
            return true

    def __len__(self) -> int:
        return 3

    def _chunk_reference_for(self, key: str) -> bytes:
        if key == '0.0':
            offset = 0
            chunksize = np.prod(self.shape) * self.dtype.itemsize
            reference = [self.path, offset, chunksize]
            return reference
        else:
            raise KeyError
