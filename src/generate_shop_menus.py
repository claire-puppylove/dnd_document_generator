import argparse
import pandas
import pathlib
# import logging
from manual_generator.html_to_pdf import html_to_pdf
from manual_generator.shop_csv_to_manual import ShopMenu
from manual_generator.markdown_html import MarkdownCompiler

# shop_1_filename = pathlib.Path("../assets/sample_shop.csv")
# shop_1_sourcefile = pandas.read_csv(shop_1_filename, sep=",", quotechar='"', quoting=0)
# shop_2_filename = pathlib.Path("../assets/sample_smith_weapons.csv")
# shop_2_sourcefile = pandas.read_csv(shop_2_filename, sep=",", quotechar='"', quoting=0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default="sample_shop")
    parser.add_argument("-t", "--title", type=str, default="Sample Shop")
    parser.add_argument("-d", "--destination", type=str, default="../manuals/")
    parser.add_argument("-s", "--sourcefile", type=str, default="../assets/sample_shop.csv")
    parser.add_argument('--pdf', action='store_true')
    parser.add_argument('--no-pdf', dest='pdf', action='store_false')
    parser.set_defaults(pdf=True)
    args = parser.parse_args()
    # logging.basicConfig(level=logging.INFO)
    # logging.info(f"Generating shop menu with args:{args}")
    print(f"Generating shop menu with args:{args}")
    filename = pathlib.Path(args.destination) / pathlib.Path(f"{args.file}.md")
    sourcefile = pathlib.Path(args.sourcefile)
    SHOP_FILE = pandas.read_csv(sourcefile, sep=",", quotechar='"', quoting=0)
    shop_menu = str(ShopMenu(SHOP_FILE, shop_name=args.title))
    with open(filename,"w") as f:
        f.write(shop_menu)
    with open(filename,"r") as f:
        md = f.read()
    html,body = MarkdownCompiler().run(md,args.title)
    with open(filename.with_suffix('.html'),"w") as f:
        f.write(html)
    if args.pdf:
        html_to_pdf(html, filename.with_name(args.title).with_suffix('.pdf'))