poetry run python src/generate_manuals.py --file "harvesting_items" --version "dm" --mode "by_item" --pdf
poetry run python src/generate_manuals.py --file "harvesting_items" --version "dm" --mode "by_monster" --pdf
poetry run python src/generate_manuals.py --file "harvesting_items" --version "player" --mode "by_item" --pdf
poetry run python src/generate_manuals.py --file "harvesting_items" --version "player" --mode "by_monster" --pdf
poetry run python src/generate_cards.py --file "harvesting_items" --pdf
poetry run python src/markdown_to_manual.py --file "dm_screen" --title "DM Screen" --pdf