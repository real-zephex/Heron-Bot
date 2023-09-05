import os
from pathlib import Path
from typing import Dict, Optional

from dotenv import dotenv_values


def read_env(path: Path, read_from_file: bool = True) -> Dict[str, Optional[str]]:
    if read_from_file is False:
        return {**os.environ}
    return {**dotenv_values(path)}
