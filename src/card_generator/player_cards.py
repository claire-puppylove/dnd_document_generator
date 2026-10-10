import os
import codecs
import markdown
import html2text
import textwrap
import re

# references: https://github.com/facelessuser/MarkdownPreview/blob/master/markdown_preview.py

def load_utf8(filename):
    """Load UTF8 file."""
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return f.read()

DEFAULT_CSS = [
        "./css/libre-baskerville.css",
        "./css/card.css",
        ]

def get_css():
    """Locate the correct CSS with the `css` setting."""
    css = DEFAULT_CSS
    css_text = []
    css_text = [
        f"<style>{load_utf8(os.path.expanduser(i))}</style>"
        for i in css
        ]
    return "\n".join(css_text)

class Card:
    '''
    Class to handle printable cards as an object

    Attributes:
        item_name:       str                : The name of the item
        storage:         str                : The item one would use to store the item
        item_type:       str                : The kind of item
        ingredient_type: str                : If used as an ingredient, things can this item make
        crafting_value:  str                : If used as an ingredient, how much money does it replace
        use:             str                : Use category of the item
        description:     str                : Effect or description of the item
        cooking_effect:  str                : Effect when cooked in a meal
        source:          str                : The source book the item is cited from
        card_class:      str                : The CSS class name for the card
    '''

    def __init__(
            self,
            item_name:str,
            storage:str,
            item_type:str,
            ingredient_type:str,
            crafting_value:str,
            use:str,
            description:str,
            cooking_effect:str,
            source:str,
            ):
        self.item_name = markdown.markdown(item_name).replace("<p>","").replace("</p>","")
        self.storage = markdown.markdown(storage).replace("<p>","").replace("</p>","")
        self.item_type = markdown.markdown(item_type).replace("<p>","").replace("</p>","")
        self.ingredient_type = markdown.markdown(ingredient_type).replace("<p>","").replace("</p>","")
        self.crafting_value = markdown.markdown(crafting_value).replace("<p>","").replace("</p>","")
        self.use = markdown.markdown(use).replace("<p>","").replace("</p>","")
        self.description = markdown.markdown(description).replace("<p>","").replace("</p>","")
        self.cooking_effect = markdown.markdown(cooking_effect).replace("<p>","").replace("</p>","")
        self.source = markdown.markdown(source).replace("<p>","").replace("</p>","")
        self.card_class = "card"
        self.text_width = 50
        self.line_limit = 30
    
    def content_to_wrapped_text(self,card_internal_html):
        # avg self.text_width chars per line
        h2t = html2text.HTML2Text()
        # h2t.body_width = self.text_width
        h2t.body_width = 0 # otherwise single_line_break is ignored >:(
        h2t.single_line_break = True
        card_text = h2t.handle(card_internal_html)\
            .strip()\
            .replace("—","--")\
            .replace("Source:","*Source:*")\
            .replace("Store in:","*Store in:*")\
            .replace("Use as ingredient for:","*Use as ingredient for:*")\
            .replace("Crafting Value (when used as ingredient):","*Crafting Value (when used as ingredient):*")\
            .replace("Use:","*Use:*")\
            .replace("Description:","*Description:*")\
            .replace("Cooking Effect:","*Cooking Effect:*")
        card_text = [cl for cl in card_text.splitlines() if cl!=""]
        wrapper = textwrap.TextWrapper(
            width=self.text_width,
            replace_whitespace=False,
            )
        card_text_wrapped = "\n".join(wrapper.fill(cl) for cl in card_text)
        return card_text_wrapped

    def card_internal_pre_split_html(self):
        # card content regardless of number of cards
        # de-dented twice (8 spaces)
        pre_split_internal = ""
        pre_split_internal+= f"<div class='section'>\n"
        pre_split_internal+= f"    <span class='subtitle'>Source:</span>\n"
        pre_split_internal+= f"    <span class='desc'>{self.source}</span>\n"
        pre_split_internal+= f"</div>\n"
        if self.storage!="-":
            pre_split_internal+= f"<div class='section'>\n"
            pre_split_internal+= f"    <span class='subtitle'>Store in:</span>\n"
            pre_split_internal+= f"    <span class='short-desc'>{self.storage}</span>\n"
            pre_split_internal+= f"</div>\n"
        if self.ingredient_type!="-":
            pre_split_internal+= f"<div class='section'>\n"
            pre_split_internal+= f"    <span class='subtitle'>Use as ingredient for:</span>\n"
            pre_split_internal+= f"    <span class='short-desc'>{self.ingredient_type}</span>\n"
            pre_split_internal+= f"</div>\n"
        if self.crafting_value!="-":
            pre_split_internal+= f"<div class='section'>\n"
            pre_split_internal+= f"    <span class='subtitle'>Crafting Value (when used as ingredient):</span>\n"
            pre_split_internal+= f"    <span class='short-desc'>{self.crafting_value}</span>\n"
            pre_split_internal+= f"</div>\n"
        if self.use!="-":
            pre_split_internal+= f"<div class='section'>\n"
            pre_split_internal+= f"    <span class='subtitle'>Use:</span>\n"
            pre_split_internal+= f"    <span class='short-desc'>{self.use}</span>\n"
            pre_split_internal+= f"</div>\n"
        if self.description != "-":
            pre_split_internal+= f"<div class='section'>\n"
            pre_split_internal+= f"    <span class='subtitle'>Description:</span>\n"
            pre_split_internal+= f"    <span class='desc'>{self.description}</span>\n"
            pre_split_internal+= f"</div>\n"
        if self.cooking_effect != "-":
            pre_split_internal+= f"<div class='section'>\n"
            pre_split_internal+= f"    <span class='subtitle'>Cooking Effect:</span>\n"
            pre_split_internal+= f"    <span class='desc'>{self.cooking_effect}</span>\n"
            pre_split_internal+= f"</div>\n"
        return pre_split_internal

    def card_start_html(self,card_num=1):
        card_start = f"<div class='cards-container'>\n"
        card_start+= f"    <div class='{self.card_class}'>\n"
        card_start+= f"        <div class='item_name'><h1>\n"
        card_start+= f"            {self.item_name}\n"
        card_start+= f"        </h1></div>\n"
        if card_num == 1:
            card_start+= f"        <div class='top-section'>\n"
            card_start+= f"            {self.item_type}\n"
            card_start+= f"        </div>\n"
        else:
            card_start+= f"        <div class='top-section'>\n"
            card_start+= f"            Continued ({card_num})\n"
            card_start+= f"        </div>\n"
        return card_start

    def card_end_html(self):
        card_end  = f"    </div>\n"
        card_end += f"</div>\n"
        return card_end 

    def split_card_internal_html(
            self,
            pre_split_internal,
            card_text_wrapped_lines,
            num_cards=1,
            ):
        # card fits self.line_limit lines after the item type and horizontal line
        split_card_internal = {card_num:"" for card_num in range(1, num_cards+1)}
        n = self.line_limit
        a = card_text_wrapped_lines
        split_wrapped_lines = [[] for i in range(num_cards)]
        remaining_split_internal = pre_split_internal
        for ln,cl in enumerate(card_text_wrapped_lines):
            cur_card = ln//n
            split_wrapped_lines[cur_card].append(cl)
        for card_num,card_lines in enumerate(split_wrapped_lines, start=1):
            last_line = [line for line in card_lines if line.strip() != ''][-1]
            last_line_html = markdown.markdown(last_line)\
                .replace("<p>","")\
                .replace("</p>","")\
                .replace("> :",">:")\
                .replace("<em>Cooking Effect:</em> ","")
            card_end_ind = remaining_split_internal.find(last_line_html)+len(last_line_html)
            card_html = remaining_split_internal[:card_end_ind]
            card_html+= "</span>\n</div>\n"
            split_card_internal[card_num] = card_html
            if card_num < num_cards:
                remaining_patch = f"<div class='section'>\n"
                remaining_patch+= f"    <span class='desc'>"
                remaining = remaining_split_internal[card_end_ind:]
                remaining = re.sub(r"^(<br>)*", '', remaining, flags=re.IGNORECASE)
                remaining_split_internal = remaining_patch + remaining
        return split_card_internal

    def __str__(self):
        # First: detect number of cards needed for this item
        # card content regardless of number of cards
        # de-dented twice (8 spaces)
        pre_split_internal = self.card_internal_pre_split_html()
        # card fits self.line_limit lines after the item type and horizontal line
        card_text_wrapped = self.content_to_wrapped_text(pre_split_internal)
        card_text_wrapped_lines = card_text_wrapped.splitlines()
        num_lines = len(card_text_wrapped_lines)
        # ceil division instead of floor
        num_cards = -(num_lines // -self.line_limit)
        if num_cards > 1:
            print(f"Warning: card text too long for card {self.item_name}, counted {num_lines} lines. Using {num_cards} cards.")
            # Second: Generate each card by looking up the last line
            # from the wrapped text in the pre-split html
            # split html and close/open spans as necessary.
            out = ""
            split_card_internal = self.split_card_internal_html(
                pre_split_internal,
                card_text_wrapped_lines,
                num_cards,
            )
            for card_num in range(1, num_cards+1):
                new_card_start = self.card_start_html(card_num)
                card_middle = textwrap.indent(split_card_internal[card_num], "        ")
                card_end = self.card_end_html()
                card_out = new_card_start + card_middle + card_end
                out+= card_out
                out+= "\n"
        else:
            new_card_start = self.card_start_html()
            card_middle = textwrap.indent(pre_split_internal, "        ")
            card_end = self.card_end_html()
            out = new_card_start + card_middle + card_end
        return out

class PrintCards:
    def get_title(self):
        """Get HTML title."""
        if self.meta_title is not None:
            title = self.meta_title
        else:
            title = self.view.name()
        if not title:
            fn = self.view.file_name()
            title = 'untitled' if not fn else os.path.splitext(os.path.basename(fn))[0]
        return '<title>%s</title>' % html.escape(title)
    def run(self, cards_html, title):
        html = '<!DOCTYPE html>'
        html += '<html><head><meta charset="utf-8">'
        html += '<meta name="viewport" content="width=device-width, initial-scale=1">'
        html += get_css()
        html += '<title>%s</title>' % title
        html += '</head><body>'
        html += cards_html
        html += '</body>'
        html += '</html>'
        return html, cards_html