import sys
import pytest
from EVA.app import App

this = sys.modules[__name__]
this.qapplication = None

@pytest.fixture(scope='session')
def qapp():
    if (this.qapplication is None):
        this.qapplication = App(sys.argv)
    yield this.qapplication