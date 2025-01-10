from pathlib import Path
import re
from rich import print

import unicodedata

def normalize(s):
    n= unicodedata.normalize('NFKD', s)
    return ''.join([c for c in n if not unicodedata.combining(c)])



output_path = Path() / "_recipes"

with Path("recipes.md").open() as f:

    new_file = True
    check_next_line = False
    write = False

    lines = f.readlines()
    for l in lines:
        if not check_next_line and re.search(r"^ *[0-9]*\.", l):
            check_next_line = True
            write = False
            continue

        if check_next_line and re.search(r"\*\*", l):
            new_file = True
            check_next_line = False
            write = True
            title =  re.sub(r"[’'*]", '', l.lower())
            filename = f"{title.replace(" ", "_").replace("\n", "")}.md"
            output_file = output_path / normalize(filename)
            print(f"[red] NEW FILE : {output_file.absolute()}")
            output_file.absolute().touch()

        if write:
            print(l)
            with output_file.absolute().open("a") as o:
                o.write(l)
