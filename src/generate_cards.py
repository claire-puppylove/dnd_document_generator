import argparse
import pandas
import pathlib
import re
# import logging
# import md_toc
from manual_generator.html_to_pdf import html_to_pdf
from manual_generator.harvesting_manual_generator import HarvestingManualGenerator
from manual_generator.player_cards import Card, PrintCards

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default="harvesting_items")
    parser.add_argument("-d", "--destination", type=str, default="../cards/")
    parser.add_argument("-t", "--title", type=str, default="Crooked Moon Harvesting Items (Player Handout Cards)")
    parser.add_argument("-s", "--sourcefile", type=str, default="../assets/monster_drops_all_dm.csv")
    parser.add_argument("-p", "--party", type=int, default=4)
    parser.add_argument('--pdf', action='store_true')
    parser.add_argument('--no-pdf', dest='pdf', action='store_false')
    parser.set_defaults(pdf=True)
    args = parser.parse_args()
    # logging.basicConfig(level=logging.INFO)
    # logging.info(f"Generating cards with args:{args}")
    print(f"Generating cards with args:{args}")
    mode = "by_monster"
    filename = pathlib.Path(args.destination) / pathlib.Path(f"{args.file}.html")
    sourcefile = pathlib.Path(args.sourcefile)
    MONSTER_DROPS = pandas.read_csv(sourcefile, sep=",", quotechar='"', quoting=0)
    player_manual = HarvestingManualGenerator(version="player",mode=mode,sourcefile=MONSTER_DROPS)
    dm_manual = HarvestingManualGenerator(version="dm",mode=mode,sourcefile=MONSTER_DROPS)
    assert len(dm_manual.items) == len(player_manual.items)
    cards = []
    for num,item in enumerate(player_manual.items):
        skip_conditions = [
            "Random" in item.item_name,
            "with alternate rolling to find options." in item.description,
            "from the Crooked Moon potions." in item.description,
            "from the Crooked Moon cursed curios." in item.description,
            "Paper" in item.item_name,
            ]
        if not any(skip_conditions):
            card = Card(
                item_name = item.item_name,
                storage = item.storage,
                item_type = item.item_type,
                ingredient_type = ", ".join(item.ingredient_type),
                crafting_value = ", ".join(item.crafting_value),
                use = ", ".join(item.use),
                description = item.description,
                cooking_effect = item.cooking_effect,
                source = ", ".join(item.source[item.monsters[0]]),
                )
            largest_amount = 1
            for dc in dm_manual.items[num].find_dc[item.monsters[0]]:
                if "1 for each party member" in dc:
                    amount = args.party
                elif "(x" in dc:
                    amount = int(re.findall(r'\(x(\d+)\)',dc)[0])
                else:
                    amount = 1
                if amount >= largest_amount:
                    largest_amount = amount
            cards.extend([str(card)]*largest_amount)
    cards_html="\n".join(cards)
    title = args.title
    html,body = PrintCards().run(cards_html, title)
    with open(filename.with_suffix('.html'),"w") as f:
        f.write(html)
    if args.pdf:
        html_to_pdf(html, filename.with_name(title).with_suffix('.pdf'))
