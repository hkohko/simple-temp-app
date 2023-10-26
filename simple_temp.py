from pathlib import Path
from subprocess import run
from sys import platform

PROJ_DIR = Path(__file__).parents[0]
python = PROJ_DIR.joinpath(".venv", "bin", "python3")
if platform == "win32":
    python = PROJ_DIR.joinpath(".venv", "Scripts", "python.exe")
app = PROJ_DIR.joinpath("src", "read_temps.py")
run([python, app])
