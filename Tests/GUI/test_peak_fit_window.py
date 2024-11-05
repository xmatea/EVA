import pytest
from pytestqt.plugin import qtbot

from EVA.app import get_app


class TestPeakFitWindow:
    # TODO add tests after making peakfit work for any data

    @pytest.fixture(autouse=True)
    def setup(self, qtbot):
        app = get_app()
        app.set_loaded_run(2630)