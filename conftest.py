import sys
import pytest
from EVA.app import App

this = sys.modules[__name__]
this.qapplication = None

"""
    This function overrides the qapp fixture used by pytest-qt when testing. Normally, pytest-qt would make an instance
    of QApplication, but we need the custom App class instead. 
"""

@pytest.fixture(scope='session')
def qapp():
    if (this.qapplication is None):
        this.qapplication = App(sys.argv) # instantiate custom App instead of QApplication
    yield this.qapplication


@pytest.fixture(scope="session")
def qapp_cls():
    return App