import argparse
import pathlib
# import md_toc
# import pdfkit
from manual_generator.markdown_html import MarkdownCompiler

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default="dm_screen")
    parser.add_argument("-t", "--title", type=str, default="DM Screen")
    parser.add_argument("-d", "--destination", type=str, default="../manuals/")
    parser.add_argument("-s", "--sourcefile", type=str, default="../assets/dm_screen.md")
    args = parser.parse_args()
    filename = pathlib.Path(args.destination) / pathlib.Path(f"{args.file}.html")
    sourcefile = pathlib.Path(args.sourcefile)
    with open(sourcefile, 'r') as f:
        md = f.read()
    html,body = MarkdownCompiler().run(md,f"Crooked Moon {args.title}")
    with open(filename.with_suffix('.html'),"w") as f:
        f.write(html)