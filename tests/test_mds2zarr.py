from fsspec.implementations.reference import ReferenceFileSystem
import pytest
import zarr
import numpy as np

from mds2zarr.mds2zarr import DataFile


def test_mds2zarr(barotropic_gyre):

    path = f'{barotropic_gyre}/Eta.0000000010.data'
    shape = (60, 60)
    dtype = ">f4"
    df = DataFile(path=path, shape=shape, dtype=dtype)

    assert len(df) == 3
    assert list(df) == ['.zarray', '.zattrs', '0.0']
    fs = ReferenceFileSystem(fo=df, target_protocol='file')
    mapper = fs.get_mapper('/')
    assert list(mapper) == ['.zarray', '.zattrs', '0.0']
    arr = zarr.open(mapper)
    assert arr.attrs['foo'] == 'bar'
    data = arr[:]
    assert data.shape == (60, 60)
    assert data.dtype == np.dtype('>f4')

    data_ref = np.fromfile(path, dtype=dtype).reshape(shape)
    np.testing.assert_equal(data, data_ref)
