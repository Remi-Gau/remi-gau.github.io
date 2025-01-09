from pathlib import Path
import re
from rich import print

with Path("recipes.md").open() as f:

    new_file = True
    check_next_line = False

    lines = f.readlines()
    for l in lines:
        if not check_next_line and re.search("^[0-9]*\.", l):
            check_next_line = True
            print(l)
            continue

        if check_next_line and re.search("^[0-9]*\.", l)
