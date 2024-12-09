# EVA - Elemental Visual Analysis
EVA is a data analysis and visualisation tool to be used with MuX at ISIS. 

# Installation guide
Download the project and unzip to a destination of your choice. 
It is highly recommended you make a virtual environment before running EVA.

Once in your virtual environment, install all requirements using the command:
```
pip install -r "requirements.txt"
```
After `pip` has installed all requirements, install an editable build of the program using the command:
```
pip install -e .
```
The above command will install a build of EVA which will update automatically as changes are made. EVA will not run unless there is a build present.

Once this is done you can start EVA by running `main.py` in src/EVA.

