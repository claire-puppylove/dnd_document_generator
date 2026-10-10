# Manual Generator

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

Clone this project and go in the manual_generator folder:

```sh
# @ shell
cd ~
git clone https://github.com/claire-puppylove/Crooked-Moon-Monster-Harvesting/
cd Crooked-Moon-Monster-Harvesting/manual_generator
```

And finally install the project

```sh
# @ shell::~/Crooked-Moon-Monster-Harvesting/manual_generator
poetry install
```

## Generator

Make a separate CSV with only the items your party has discovered. For example, I made `../assets/monster_drops_chapter_1_example.csv` copying only the rows with items from until after the Ghostlight Locomotive fight.

First make a folder to output your new files (in my case I already made this):

```sh
# @ shell
mkdir ../example_handouts/
```

Then run the generator like so:

```sh
# @ shell

poetry run python ./src/generate_manuals.py \
--file "chapter1_drops" \
--version "player" \
--mode "by_item" \
--destination "../example_handouts/" \
--sourcefile "../assets/monster_drops_chapter_1_example.csv"
```

Where:
- `--file` is the output file name without extensions (since I use both .md and .html)
- `--version` is either `"dm"` or `"player"`
- `--mode` is either `"by_item"` or `"by_monster"`
- `--destination` is the directory where the files will be output to
- `--sourcefile` is the CSV that you will use to make the modified manual

This should make a markdown and an HTML file automatically with only the items in your CSV file. Note that changing the number of columns or their names will make the program have errors.