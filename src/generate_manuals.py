import argparse
import pandas
import pathlib
# import logging
# import md_toc
from manual_generator.html_to_pdf import html_to_pdf
from manual_generator.harvesting_manual_generator import HarvestingManualGenerator
from manual_generator.markdown_html import MarkdownCompiler

FILE_README = pathlib.Path("../README.md")
with open(FILE_README, 'r') as f:
    README = f.read()
FILE_README_PLAYER = pathlib.Path("../README_player.md")
with open(FILE_README_PLAYER, 'r') as f:
    README_PLAYER = f.read()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default="harvesting_items")
    parser.add_argument("-v", "--version", type=str, default="dm")
    parser.add_argument("-m", "--mode", type=str, default="by_item")
    parser.add_argument("-t", "--title", type=str, default="")
    parser.add_argument("-d", "--destination", type=str, default="../manuals/")
    parser.add_argument("-s", "--sourcefile", type=str, default="../assets/monster_drops_all_dm.csv")
    parser.add_argument('--readme', action='store_true')
    parser.add_argument('--no-readme', dest='readme', action='store_false')
    parser.set_defaults(readme=True)
    parser.add_argument('--pdf', action='store_true')
    parser.add_argument('--no-pdf', dest='pdf', action='store_false')
    parser.set_defaults(pdf=True)
    args = parser.parse_args()
    # logging.basicConfig(level=logging.INFO)
    # logging.info(f"Generating harvesting manual with args:{args}")
    print(f"Generating harvesting manual with args:{args}")
    filename = pathlib.Path(args.destination) / pathlib.Path(f"{args.file}_{args.version}_{args.mode}.md")
    sourcefile = pathlib.Path(args.sourcefile)
    MONSTER_DROPS = pandas.read_csv(sourcefile, sep=",", quotechar='"', quoting=0)
    readme=""
    if args.readme==True:
        if args.version=="dm":
            readme+= README
        elif args.version=="player":
            readme+= README_PLAYER
    readme+= "\n  \n\n"
    manual = str(HarvestingManualGenerator(version=args.version,mode=args.mode,sourcefile=MONSTER_DROPS))
    with open(filename,"w") as f:
        f.write(manual)
        # #insert Table of Contents
        # toc = md_toc.api.build_toc(filename)
        # md_toc.api.write_string_on_file_between_markers(filename, toc, '<!-- TOC -->')
    with open(filename,"r") as f:
        md = f.read()
    title = f"Crooked Moon Harvesting Items {args.title}({args.version} - {args.mode.replace("_"," ")})"
    html,body = MarkdownCompiler().run(md,title)
    _,readme_body = MarkdownCompiler().run(readme,"")
    readme_insert = """<div class="wide">""" + readme_body + "</div>"
    insert_index = html.find("""<body><article class="markdown-body">""")+len("""<body><article class="markdown-body">""")
    out_html = html[:insert_index] + readme_insert + html[insert_index:]
    with open(filename.with_suffix('.html'),"w") as f:
        f.write(out_html)
    if args.pdf:
        html_to_pdf(out_html, filename.with_name(title).with_suffix('.pdf'))