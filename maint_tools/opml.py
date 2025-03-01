import listparser
from pathlib import Path

root_folder = Path(__file__).parents[1]

opml_file = root_folder / "OPML_export_20250301_202833.opml"

result = listparser.parse(opml_file.open().read())


content = """---
layout: default
title: Podcasts roll
permalink: /podcasts.html
---

<div class="row">
    <div class="col-12 text-center">
        <div class="navy-line"></div>
        <h1>Podcasts I listen to.</h1>
    </div>

    <div class="post-content">

    <div class="col-12 text-center">
        <p>I use <a href="https://podcastaddict.com/">PodcastAddict</a> to manage my subscriptions.</p>
    </div>

    <div class="row justify-content-center">
    <div class="col-8">
        <ul>
"""

for x in result.feeds:
    content += f"            <li> <a href='{x.url}'>{x['title']}</a> </li>\n"

content += """
        </ul>
    </div>
    </div>
    </div>
</div>
"""

oupout_file = root_folder / "podcasts.html"
with oupout_file.open("w") as f:
    f.write(content)
