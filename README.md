# EVA - Elemental Visual Analysis
EVA is a data analysis and visualisation tool to be used with MuX at ISIS. 

---
# User Manual
A full user manual can be found in EVA under the "Help" tab. Alternatively you can find the HTML manual [here](src/EVA/resources/manual/manual.html) - just open it with a browser.

---
# Installing and building EVA from source
Download the project and unzip to a destination of your choice. 
It is highly recommended you make a virtual environment before running EVA.

Once in your virtual environment, install all requirements:
```
pip install -r "requirements.txt"
```
After `pip` has installed all requirements, install an editable build of the program:
```
pip install -e .
```
The above command will install a build of EVA which will update automatically as changes are made. EVA will not run unless there is a build present.

Once this is done you can start EVA by running `main.py` in src/EVA.

## How to build the .exe
EVA uses Pyinstaller to compile the python script into an executable file. To build the executable, run
```
pyinstaller EVA.spec
```

Use the flag `--noconfirm` if you want to ignore the overwrite warning.

After this you can find the EVA.exe in the `dist` folder at root level.