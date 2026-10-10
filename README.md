# Game Documents Generator

I made a few methods to make Markdown documents of the CSV for readability.

You don't need to install it for the full manuals I already provide in `/manuals`, but if you do want to make smaller handouts to your players with only the items they've discovered so far, you might want to install it. This project uses python with Poetry. You don't need to know Python to install this, but you need to be comfortable with a terminal.

Alternatively, if you really want to make a handout for your players but don't want to install it, you can just duplicate the manual files I have and delete the extra information using a text editor.

## Dependencies

Install pyenv (to be able to install python)

```sh
# @ shell(linux/mac_osx/wsl)

cd ~
git clone --depth=1 https://github.com/pyenv/pyenv.git ~/.pyenv
cd ~/.pyenv && src/configure && make -C src
cd ~
source ~/.bash_profile

echo '' >> ~/.bash_profile
echo '# Install pyenv to ~/.pyenv' >> ~/.bash_profile
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile

source ~/.bash_profile
```

Install python with pyenv:

```sh
# @ shell(linux/mac_osx/wsl)

pyenv install 3.12.11
pyenv global 3.12.11
pyenv rehash
```

Install pipx (to be able to install Poetry):

```sh
# @ shell(linux/wsl)

sudo apt-get update
sudo apt-get install pipx

# @ shell(mac_osx)

brew install pipx
```

Install Poetry with pipx

```sh
# @ shell

pipx install poetry && pipx inject poetry poetry-plugin-export
```

Clone this project and go in the `game_documents_generator` folder:

```sh
# @ shell
cd ~
git clone https://github.com/claire-puppylove/Crooked-Moon-Monster-Harvesting/
cd Crooked-Moon-Monster-Harvesting/game_documents_generator
```

And install the project

```sh
# @ shell::~/Crooked-Moon-Monster-Harvesting/game_documents_generator
poetry install
```

When using `weasyprint` as the PDF backend, there are no further dependencies.

If you prefer `pyhtml2pdf`, `playwright`, or `pdfkit`, I left the code to use them but you must install their dependencies separately.

## Generator

### Monster Drops manual and cards

Make a separate CSV with only the items your party has discovered. For example, I made `../assets/monster_drops_chapter_1_example.csv` copying only the rows with items from until after the Ghostlight Locomotive fight.

First make a folder to output your new files (in my case I already made this):

```sh
# @ shell::~/Crooked-Moon-Monster-Harvesting/game_documents_generator
mkdir ../example_handouts/
```

#### Harvesting Manual

Then run the generator like so:

```sh
# @ shell::~/Crooked-Moon-Monster-Harvesting/game_documents_generator

poetry run python ./src/generate_manuals.py \
--file "chapter1_drops" \
--version "player" \
--mode "by_item" \
--title "Chapter 1 drops" \
--destination "../example_handouts/" \
--sourcefile "../assets/monster_drops_chapter_1_example.csv" \
--pdf
```

Where:
- `--file` is the output file name without extensions (since I use both .md and .html)
- `--version` is either `"dm"` or `"player"`
- `--mode` is either `"by_item"` or `"by_monster"`
- `--title` is the name suffix added to the title in the HTML, as well as the filename in the PDF
- `--destination` is the directory where the files will be output to
- `--sourcefile` is the CSV that you will use to make the modified manual
- `--pdf` activates the PDF output

This should make a markdown and an HTML file automatically with only the items in your CSV file. Note that changing the number of columns or their names will make the program have errors.

#### Cards

For the cards, run the generator like so:

```sh
# @ shell
poetry run python ./src/generate_cards.py \
--file "chapter1_drops" \
--title "Chapter 1 drops (handout cards)" \
--sourcefile "../assets/monster_drops_chapter_1_example.csv" \
--destination "../example_handouts" \
--party 4 \
--overridemaxrepeats 4 \
--pdf
```

Where:
- `--file ` is the output file name without extensions (since I use both .md and .html)
- `--title ` is the name suffix added to the title in the HTML, as well as the filename in the PDF
- `--sourcefile ` is the CSV that you will use to make the cards document
- `--destination ` is the directory where the files will be output to
- `--party ` is the number of party members used where the number of cards is listed as "1 per party member" in the CSV
- `--overridemaxrepeats ` is the maximum number of times a card will be repeated in the entire document, used to avoid printing a ton of common drops like paper or ammo
- `--pdf ` activates the PDF output


### Shop menus and cards

Make a separate CSV with items in a shop. For example, I made `../assets/sample_shop.csv` and `sample_smith_weapons.csv`.

There are **3 minimum columns** with specific names that the CSV should have.

- An item name column named whichever of the following `["Name","name"]`
- A price column named whichever of the following `["Cost","cost","Price","price","Value","value"]`
- An item description column named whichever of the following `["Description","description"]`

#### Shop Menu

Then run the generator like so:

```sh
# @ shell::~/Crooked-Moon-Monster-Harvesting/game_documents_generator
poetry run python src/generate_shop_menus.py \
--sourcefile "../assets/sample_shop.csv" \
--file "sample_shop" \
--title "Sample Shop" \
--destination "../example_handouts/" \
--pdf
```

Where:
- `--file` is the output file name without extensions (since I use both .md and .html)
- `--title` is the name suffix added to the title in the HTML, as well as the filename in the PDF
- `--destination` is the directory where the files will be output to
- `--sourcefile` is the CSV that you will use to make the modified manual
- `--pdf` activates the PDF output

This should make a markdown and an HTML file automatically with only the items in your CSV file. Note that using a CSV without at least the 3 columns specified above will make the program have errors.

#### Shop Cards

For the cards, run the generator like so:

```sh
# @ shell::~/Crooked-Moon-Monster-Harvesting/game_documents_generator
poetry run python src/generate_shop_cards.py \
--sourcefile "../assets/sample_shop.csv" \
--file "sample_shop_cards" \
--title "Sample Shop Cards" \
--destination "../cards/" \
--pdf
```

Where:
- `--file ` is the output file name without extensions (since I use both .md and .html)
- `--title ` is the name suffix added to the title in the HTML, as well as the filename in the PDF
- `--sourcefile ` is the CSV that you will use to make the cards document
- `--destination ` is the directory where the files will be output to
- `--pdf ` activates the PDF output

### Any Markdown to a Manual

For the DM Screen I also programmed a generic Markdown to Manual converter. It will generate HTML based on the markdown and use the same CSS as everything else, then generate a PDF with WeasyPrint.

Run the generator like so:

```sh
# @ shell::~/Crooked-Moon-Monster-Harvesting/game_documents_generator
poetry run python src/markdown_to_manual.py \
--sourcefile "../assets/dm_screen.md" \
--file "dm_screen" \
--title "DM Screen" \
--destination "../manuals/"
--pdf
```

Where:
- `--file ` is the output file name without extensions (since I use both .md and .html)
- `--title ` is the name suffix added to the title in the HTML, as well as the filename in the PDF
- `--sourcefile ` is the CSV that you will use to make the cards document
- `--destination ` is the directory where the files will be output to
- `--pdf ` activates the PDF output