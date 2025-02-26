
# EVA developer documentation

Last updated 1/10/2024

By Matea Bjørklund

# Table of contents

1. [Overview](#Overview)
- [File structure](#file-structure)
- [Building EVA](#building-eva)

2. [Program structure](#program-structure)

i- pp.py](#custom-classes)
 [main.p(#config-files)
	
- [Main window and other windows](#mainwindow.py-and-other-windows)
	
- [Future improvements](#future-improvements)

3. [Data structures](#data-structures)
	
- [The Dataset class](#the-dataset-class)
	
- [The Run class](#the-run-class)
	
- [The Detector Enum class](#the-detector-enum-class)

4. [Unit testing](#unit-testing)
	
- [Making tests work with the custom app class](#making-tests-work-with-the-custom-app-class)
	
- [Cleaning up after tests](#cleaning-up-after-tests)

5. [Config files](#config-files)

# Overview

### File structure

EVA source code is located under src/EVA/. This file structure was implemented as it is the recommended structure for scientific packages according to [PyOpenSci]([[https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-structure.html](](https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-structure.html%5D()[https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-structure.html)](https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-structure.html))). Although EVA is not quite a scientific package, this structure plays well with build tools.

The idea with the src directory is to keep all code that is essential for EVA to run inside, and nothing else. The unit tests and test data are therefore located outside the src directory. Running unit tests outside the source directory allows for more accurate testing, and keeps the size of the actual program smaller.

The src directory also contains a modified version of [pysrim]([[https://github.com/costrouc/pysrim](](https://github.com/costrouc/pysrim%5D()[https://github.com/costrouc/pysrim)](https://github.com/costrouc/pysrim))). Due to an update in PyYAML, the following modification has to be made in the pysrim/core/elementdb.py file (as of 28/10/24) in order for it to work properly.

From

```py

def create_elementdb():
dbpath = os.path.join(srim.__path__[0], 'data', 'elements.yaml')
return yaml.load(open(dbpath, "r"))

```

To

```py

def create_elementdb():
	
dbpath = os.path.join(srim.__path__[0], 'data', 'elements.yaml')
	
return yaml.load(open(dbpath, "r"), Loader=yaml.FullLoader)

```

This modification has been made to the copy of pysrim located under src/, but the copy can be removed in the future if the error is patched in the original .

### Building EVA

Currently there is no "production build" of EVA. In the future, some library could be used to export the code into an .exe file, but for now all users  developers will have to build and run EVA through either command line or using an IDE. Details on how to build and run EVA can be found in the EVA README.md.

# Program structure

# pp.py

The App class is a QApplication subclass which provides the framework for EVA. It is a singleton instance and can be accessed anywhere in the code, so it is used to hold important global context such as settings, databases and loaded user data. It replaces the previous globals.py file, and more functionality could be added to the app class in the future. A nice example of using a app class can be found [here]([https://github.com/OpenShot/openshot-qt/blob/develop/src/classes/app.py](https://github.com/OpenShot/openshot-qt/blob/develop/src/classes/app.py)).

The app instance can be quickly accessed anywhere by calling `QApplication.instance()` or using the wrapper function `get_app()` from app.py. The App class also has a wrapper function `get_config()` which returns the current config.

app.py

```py

def get_app():
	
return QApplication.instance()

def get_config():
	
return get_app().config

```

**NOTE**: Be aware that `get_app()` doesn't return a copy of the app, but a reference to the main instance, so if you modify any of the variables within the app such as `app.config` or `app.loaded_run`, they will be modified everywhere.

---

If you want to add methods to the app class, be careful to avoid circular imports. For example, if you want to add a method that loads data so that you can do `app.load_run(run_number)` and call some other file `load_run.py` automatically, you need to make sure `load_run.py` doesn't require `app.py`, otherwise the program will error.

## main.py

This is the entry point of the program which makes the App instance and runs it. (This was previously in MainWindow.py) Other things could be added in there in the future, such as starting up logging tools.

## MainWindow.py and other windows

This file contains the code for the main window of . This is the main window, and all other windows are launched through this window. All windows except MainWindow are QWidgets. MainWindow creates instances of the QWidgets without a parent and calls `show()` on them, which forces Qt to display the widgets as separate windows. (this is the default behaviour of Qt).

Each window can access the global context by calling get_app() or get_config().

## Future improvements

Currently, most of the xxxx_window.py files contain both GUI code and logic. This is generally bad practice for large applications, but it's fine at the moment as EVA is quite small. In the future though it could be good to look into a more structured layout, for example a MVP or [MVVM]([https://medium.com/@mark_huber/a-clean-architecture-for-a-pyqt-gui-using-the-mvvm-pattern-b8e5d9ae833d](https://medium.com/@mark_huber/a-clean-architecture-for-a-pyqt-gui-using-the-mvvm-pattern-b8e5d9ae833d)) layout to separate the GUI and the logic. Also, if more complex GUIs are made using QtDesigner, they'll be added as .ui files, which will force separation of GUI and logic.

# Custom classes

## Data structures

EVA uses two custom data structures when loading data into the program. Their definitions can be found in src/EVA/data_structures.py.

### The Dataset class

The dataset class holds data from a single spectrum, for a single detector.

data_structures.py

```py

@dataclass

class Dataset:
	
"""
	
The 'Dataset' class holds the data from a single detector for a single run.
	
It holds the x and y data as numpy arrays.
	
It also holds the run number and detector the dataset came from.
	
"""
	
detector: str
	
run_number: str
	
x: np.ndarray
	
y: np.ndarray

```

The @dataclass decorator was used because Dataset is just a data container - this just reduces some boilerplate code. Dataset behaves just like a regular class, but has no methods.

### The Run class

The Run class contains the spectra from all the detectors for a given run. It stores a copy of the raw data as well as the normalised / energy corrected data. It also holds metadata such as normalisation type applied and the information from comment.dat file, if present.

data_structures.py

```py

class Run:
	
def __init__(self, raw: list[Dataset], loaded_detectors: list[str],
	 run_num: str, 

start_time: str, end_time: str, eventr_str: str, 
	 comment: str):

		 # Main data containers and essential info
		
 self.raw = raw
		
 self.data = deepcopy(raw)
		
 self.loaded_detectors = loaded_detectors
		
 self.run_num = run_num

		 # Metadata from comment file (may not be available)
		
 self.start_time = start_time
		
 self.end_time = end_time
		
 self.events_str = events_str
		
 self.comment = comment

		 # Normalisation and energy correction info
		
 self.normalisation = None
		
 self.normalise_which = []
		
 self.e_corr_params = None
		
 self.e_corr_which = []

```

`self.raw` and `self.data` are lists of Datasets. They have a fixed size, with index 0 corresponding to the Ge1 Dataset and index 7 corresponding to Ge8. If no data is present for a detector, an empty Dataset will be at that index.

The normalisation and energy correction information should **NOT** be modified directly. Instead, they should be modified through the set_normalisation() and set_energy_corrction() methods within the Run class. This ensures that there is never a mismatch between the specified normalisation status and the actual normalisation applied.

### The Detector Enum class

There is an Enum class in `data_structures.py` which can be used if a spectrum has to be indexed from `raw` or `data` by name, rather than index number:

data_structures.py

```py

class Dataset(Enum):

GE1 = 0

GE2 = 1

GE3 = 2

GE4 = 3

GE5 = 4

GE6 = 5

GE7 = 6

GE8 = 7

```

Example usage:

```py

from data_structures import Detector

# The below are equivalent

GE1_dataset = run.data[0]

GE1_dataset = run.data[Detector.GE1]

# Useful if you need to index by detector name:

name = "GE1"

GE1_dataset = run.data[Detector[name]]

```

This may not be needed for most cases, but there could be certain situations where you would have to pick out a Dataset from a Run by name rather than index, and you need the name to be a variable.

## The PlotWidget class

The PlotWidget class is used for creating matplotlib figures which can easily be embedded into Qt layouts as a QWidget. A PlotWidget contains a [FigureCanvas]([https://matplotlib.org/stable/api/backend_qt_api.html](https://matplotlib.org/stable/api/backend_qt_api.html)) which provides the matplotlib backend, and [navigation toolbar]([https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_qt_sgskip.html](https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_qt_sgskip.html)). To create a PlotWidget, create your figure and axes `fig` and `axs` with pyplot as you normally would, but instead of showing the figure using fig.show(), create a plotwidget instead and add it to your layout.

```py

fig, axs = plt.subplots(nrows=2)

fig.suptitle("title")

axs[0].plot(x1, y1)

axs[1].plot(x2, y2)

plot = PlotWidget(fig, axs)

some_layout.addWidget(plot)

```

Alternatively you can create an empty PlotWidget and update it later.

```py

plot = PlotWidget()

some_layout.addWidget(plot)

# later on

fig, ax = ...

plot.update_plot(fig, ax)

```

# Unit testing

All unit tests are run outside of the src directory. The test suite uses [pytest]([https://docs.pytest.org/en/stable/](https://docs.pytest.org/en/stable/)), but some older tests use unittest. pytest is compatible with unittest, so running pytest will also run the older tests without problem. The [pytest-qt]([https://pytest-qt.readthedocs.io/en/latest/intro.html](https://pytest-qt.readthedocs.io/en/latest/intro.html)) library is used for testing the pyqt-specific parts of the program.

## Making tests work with the custom app class

pytest-qt provides the qtbot fixture, which when passed as an argument to a test, will create an instance of the application. However, since EVA uses a subclass of QApplication, the `conftest.py` file in the root directory is required to force pytest-qt to use the custom class rather than the default QApplication. The consequence of this is that **all tests that require access to the app must take in the qtbot or qapp fixture as an argument**, otherwise get_app() will return none. If you're doing GUI testing, use qtbot, otherwise use qapp (`from pytestqt.plugin import qapp`).

```py

def test_something(qtbot):
	
app = get_app()
	
qtbot.click(something)
	
assert something
	
OR

def test_something_else(qapp):
	
app = get_app()
	
assert something

```

However, if you are using a setup fixture with `autouse=True`, you only need to pass qtbot or qapp as a fixture to the setup function, since the function will execute before all your tests and therefore start up the correct App class.

```py

@pytest.fixture(autouse=True)

def setup(qtbot):
	do something

def test_something():
	app = get_app()
	assert something
```

## Cleaning up after tests

Pytest-qt does not automatically reset the app state in between tests. Example:

```py
def test_1(qapp):
	app = get_app()
	app.param = "changed"

def test_2(qapp):
	app = get_app()
	print(app.param) # will return `changed`
```

So if you modify the app state, make sure to reset it in between tests.

# Config files

EVA uses the `configparser` library for configurations, which is included in the Python standard library. All user configurations are stored in EVA/src/config.ini. The default configs are stored in EVA/src/default.ini. Configparser loads the configurations from the files into a dictionary-like object. You can read about configparser [here].

The Config class (defined in config.py) is the "config manager" of the program. It stores the `configparser` under the `parser` attribute and has some utility methods to save current config to file or restore default settings. On startup, configparser will read config.ini and store the result as a Config object in the app under app.config. The Config object can then be accessed anywhere using `app.get_config()`.

Normally you'd access the configuration values like this:

```py
from EVA.app import get_config()
config = get_config()
value = config.parser[section][field] # this works
```

But the `__getattr__()` magic function in Config allows you to access the configparser directly when indexing the Config object itself:

```py
value = config[section][field] # this works too!
```

But if you want to call a built-in method from the configparser library you have to explicitly call it on config.parser:

```py
config.parser.some_method()
```

---

Although configparser is very easy to use, one major disadvantage with it is that it can only read and write strings. This isn't too much of an issue for ints and booleans, but if you want to store an array, the easiest way to do this is to store the array as:

```ini
[arrays]
arr = 1 2 3 4
```

Then, you can get the array from the config using `arr = config[arrays][arr].split(" ")` or use the `to_array()` method in Config. If this becomes a big issue in the future, consider switching from configparser to tomllib.

---

Side note: remember to put config.ini in your .gitignore so you don't accidentally commit your configs.