import argparse
import pandas
import pathlib
# import logging
from manual_generator.html_to_pdf import html_to_pdf
from manual_generator.shop_csv_to_manual import ShopMenu
from manual_generator.player_cards import Card, PrintCards
from manual_generator.markdown_html import MarkdownCompiler

# shop_1_filename = pathlib.Path("../assets/sample_shop.csv")
# shop_1_sourcefile = pandas.read_csv(shop_1_filename, sep=",", quotechar='"', quoting=0)
# shop_2_filename = pathlib.Path("../assets/sample_smith_weapons.csv")
# shop_2_sourcefile = pandas.read_csv(shop_2_filename, sep=",", quotechar='"', quoting=0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default="sample_shop")
    parser.add_argument("-t", "--title", type=str, default="Sample Shop Cards")
    parser.add_argument("-d", "--destination", type=str, default="../cards/")
    parser.add_argument("-s", "--sourcefile", type=str, default="../assets/sample_shop.csv")
    parser.add_argument('--pdf', action='store_true')
    parser.add_argument('--no-pdf', dest='pdf', action='store_false')
    parser.set_defaults(pdf=True)
    args = parser.parse_args()
    # logging.basicConfig(level=logging.INFO)
    # logging.info(f"Generating shop menu with args:{args}")
    print(f"Generating shop cards with args:{args}")
    filename = pathlib.Path(args.destination) / pathlib.Path(f"{args.file}.md")
    sourcefile = pathlib.Path(args.sourcefile)
    SHOP_FILE = pandas.read_csv(sourcefile, sep=",", quotechar='"', quoting=0)
    shop_menu = ShopMenu(SHOP_FILE, shop_name=args.title)
    cards = []
    for num,item in enumerate(shop_menu.shop_items):
        skip_conditions = [
            "Random" in item.item_name,
            "with alternate rolling to find options." in item.description,
            "from the Crooked Moon potions." in item.description,
            "from the Crooked Moon cursed curios." in item.description,
            "Paper" in item.item_name,
            ]
        if not any(skip_conditions):
            if "storage" in item.details:
                storage = item.details["storage"]
            elif "Storage" in item.details:
                storage = item.details["Storage"]
            else:
                storage = "-"
            if "item_type" in item.details:
                item_type = item.details["item_type"]
            elif "Type" in item.details:
                item_type = item.details["Type"]
            else:
                item_type = "-"
            if "ingredient_type" in item.details:
                ingredient_type = item.details["ingredient_type"]
            else:
                ingredient_type = "-"
            if "use" in item.details:
                use = item.details["use"]
            elif "Use" in item.details:
                use = item.details["Use"]
            else:
                use = "-"
            if "cooking_effect" in item.details:
                cooking_effect = item.details["cooking_effect"]
            else:
                cooking_effect = "-"
            if "source" in item.details:
                source = item.details["source"]
            elif "Source" in item.details:
                source = item.details["Source"]
            else:
                source = "-"
            description = ""
            exc = [
                "storage",
                "Storage",
                "item_type",
                "Type",
                "ingredient_type",
                "use",
                "Use",
                "cooking_effect",
                "source",
                "Source",
                ]
            for key,det in item.details.items():
                if det != "" and det != "-":
                    if key not in exc:
                        description += f"__{key}__: {det}  \n"
            if item.description != "" and item.description != "-":
                description += f"{item.description} \n"
            crafting_value = f"Half of cost: {item.cost}"
            card = Card(
                item_name = item.item_name,
                storage = storage,
                item_type = item_type,
                ingredient_type = ingredient_type,
                crafting_value = crafting_value,
                use = use,
                description = description,
                cooking_effect = cooking_effect,
                source = source,
                )
            largest_amount = 1
            cards.extend([str(card)]*largest_amount)
    cards_html="\n".join(cards)
    title = args.title
    html,body = PrintCards().run(cards_html, title)
    with open(filename.with_suffix('.html'),"w") as f:
        f.write(html)
    if args.pdf:
        html_to_pdf(html, filename.with_name(title).with_suffix('.pdf'))