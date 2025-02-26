import pytest
from pytestqt.plugin import qtbot

from EVA.core.app import get_app


class TestPeakFitWindow:
    # TODO add tests after making peakfit work for any data

    @pytest.fixture(autouse=True)
    def setup(self, qtbot):
        pass