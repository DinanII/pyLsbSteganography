# Demo Steganography script written in Python

## Steganography
> "Steganography is the process of hiding a secret message within a larger one in such a way that someone can not know the presence or contents of the hidden message."
-- [TowardsDataSience.com](https://towardsdatascience.com/hiding-data-in-an-image-image-steganography-using-python-e491b68b1372)

## Brief setup summary
1. Initiate a virtual enviroment with: `python3 -m venv .env` or `python -m venv .env` (for Windows). 
This will initiate a new virtual enviroment locally. Please use the interpeter included in the virtual enviroment (.env/bin/python).
2. Activate virtual enviroment
    - **Windows**
        - CMD: `.env/Scripts/activate.bat`.
        - Powershell: `.env/Scripts/Activate.ps1`.
        - Powershell Core: `.env/bin/Activate.ps1`.
    - **Mac and Linux**
        - Bash and ZSH: `source .env/bin/activate`.
        - Fish: `source .env/bin/activate.fish`.
        - csh/tcsh: `source .env/bin/activate.csh`.
    To deactivate the virtual enviroment, execute the `deactivate` command.
3. Install packages with: `pip install -r requirements.txt`. 
This will install all packages listed in __{project_root}/requirements.txt__.
4. If a new dependency is installed, run `pip freeze > requirements.txt` so every package (including new ones) is registered, so others
can also easily install.
5. The Python Tkinter module is required for the file dialogs. Cannot be installed in local enviroment via pip. But can be installed globally with:
    - Ubuntu: `sudo apt-get install python3-tk`.
    - Windows: `pip install tk`