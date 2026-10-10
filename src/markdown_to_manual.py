import argparse
import pathlib
# import md_toc
from manual_generator.html_to_pdf import html_to_pdf
from manual_generator.markdown_html import MarkdownCompiler

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default="dm_screen")
    parser.add_argument("-t", "--title", type=str, default="DM Screen")
    parser.add_argument("-d", "--destination", type=str, default="../manuals/")
    parser.add_argument("-s", "--sourcefile", type=str, default="../assets/dm_screen.md")
    parser.add_argument('--pdf', action='store_true')
    parser.add_argument('--no-pdf', dest='pdf', action='store_false')
    parser.set_defaults(pdf=True)
    args = parser.parse_args()
    filename = pathlib.Path(args.destination) / pathlib.Path(f"{args.file}.html")
    sourcefile = pathlib.Path(args.sourcefile)
    with open(sourcefile, 'r') as f:
        md = f.read()
    title = f"Crooked Moon {args.title}"
    html,body = MarkdownCompiler().run(md,title)
    with open(filename.with_suffix('.html'),"w") as f:
        f.write(html)
    if args.pdf:
        html_to_pdf(html, filename.with_name(title).with_suffix('.pdf'))