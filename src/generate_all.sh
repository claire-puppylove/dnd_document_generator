poetry run python src/generate_manuals.py --file "harvesting_items" --version "dm" --mode "by_item" --pdf
poetry run python src/generate_manuals.py --file "harvesting_items" --version "dm" --mode "by_monster" --pdf
poetry run python src/generate_manuals.py --file "harvesting_items" --version "player" --mode "by_item" --pdf
poetry run python src/generate_manuals.py --file "harvesting_items" --version "player" --mode "by_monster" --pdf
poetry run python src/generate_cards.py --file "harvesting_items" --pdf
poetry run python src/markdown_to_manual.py --sourcefile "../assets/dm_screen.md" --file "dm_screen" --title "DM Screen" --pdf
poetry run python src/generate_shop_menus.py --sourcefile "../assets/sample_shop.csv" --file "sample_shop" --title "Sample Shop" --pdf
poetry run python src/generate_shop_menus.py --sourcefile "../assets/sample_smith_weapons.csv" --file "sample_smith_weapons" --title "Sample Smith Weapons" --pdf
poetry run python src/generate_shop_cards.py --sourcefile "../assets/sample_shop.csv" --file "sample_shop_cards" --title "Sample Shop Cards" --pdf
poetry run python src/generate_shop_cards.py --sourcefile "../assets/sample_smith_weapons.csv" --file "sample_smith_weapons_cards" --title "Sample Smith Weapons Cards" --pdf
poetry run python src/generate_manuals.py --file "chapter1_drops" --version "player" --mode "by_item" --title "Chapter 1 drops" --sourcefile "../assets/monster_drops_chapter_1_example.csv" --destination "../example_handouts" --pdf
poetry run python src/generate_cards.py --file "chapter1_drops" --title "Chapter 1 drops (handout cards)" --sourcefile "../assets/monster_drops_chapter_1_example.csv" --destination "../example_handouts" --pdf