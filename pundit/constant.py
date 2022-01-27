import os
from pathlib import Path

PATH_BASE = Path(os.path.dirname(__file__))
PATH_GUI = PATH_BASE / "gui"
PATH_EXPERIMENTS = PATH_GUI / "experiments"
PATH_RESULTS = PATH_GUI / "results"
