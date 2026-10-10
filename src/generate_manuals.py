import argparse
import pathlib
# import md_toc
# import pdfkit
from manual_generator.manual_generator import ManualGenerator
from manual_generator.markdown_html import MarkdownCompiler

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default="harvesting_items")
    parser.add_argument("-v", "--version", type=str, default="dm")
    parser.add_argument("-m", "--mode", type=str, default="by_item")
    parser.add_argument("-d", "--destination", type=str, default="../manuals/")
    args = parser.parse_args()
    filename = pathlib.Path(args.destination) / pathlib.Path(f"{args.file}_{args.version}_{args.mode}.md")
    out = str(ManualGenerator(version=args.version,mode=args.mode))
    with open(filename,"w") as f:
        f.write(out)
        # #insert Table of Contents
        # toc = md_toc.api.build_toc(filename)
        # md_toc.api.write_string_on_file_between_markers(filename, toc, '<!-- TOC -->')
    with open(filename,"r") as f:
        md = f.read()
    html,body = MarkdownCompiler().run(md,f"Crooked Moon Harvesting Items ({args.mode.replace("_"," ")})")
    with open(filename.with_suffix('.html'),"w") as f:
        f.write(html)
    # pdfkit.from_string(html, filename.with_suffix('.pdf'))