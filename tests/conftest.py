import py

import pooch
import pytest
import os


def _clean_files(filelist):
    # remove all the crud from the test directories 😩
    for fname in filelist:
        basename = os.path.basename(fname)
        dirname = os.path.dirname(fname)
        if basename.startswith('.') or ('CVS' in dirname):
            os.remove(fname)
        else:
            good_dirname = dirname
    return good_dirname


@pytest.fixture(scope="session")
def barotropic_gyre():
    import pooch
    POOCH = pooch.create(
        path=pooch.os_cache("mitgcm-test-data"),
        base_url="doi:10.6084/m9.figshare.7571828.v1/",
        registry={
            "barotropic_gyre.tar.gz": "807ac448fbfcebf9822fdd2b81c35e4f8c68c9998374d15ef6a71bc07293dd8e"
        }
    )

    filelist = POOCH.fetch(
        'barotropic_gyre.tar.gz',
        processor=pooch.Untar()
    )

    return _clean_files(filelist)
