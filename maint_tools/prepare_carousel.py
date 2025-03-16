"""Move pictures and create yaml listing."""

from utils import root_folder, static_folder
from yaml import dump

output = [
    {"src": f"carousel/{image.name}", "title": image.stem}
    for image in (static_folder / "assets" / "img" / "carousel").glob("*.jpg")
]
output.extend(
    [
        {"src": f"carousel/{image.name}", "title": image.stem}
        for image in (static_folder / "assets" / "img" / "carousel").glob(
            "*.png"
        )
    ]
)


with (root_folder / "_data" / "index" / "banners.yml").open("w") as f:
    dump(output, f)
