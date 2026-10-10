import os
import codecs
import markdown

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
        card_length:     str                : The CSS class used for card length for properly formatting font size
    
    Notes:
        - description+cooking effect <= 1150 character limit for CSS class card 
        - description+cooking effect <= 2200 for CSS class card-long
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
        # length = len(self.description)+len(self.cooking_effect)
        # self.card_length = "card" if length <= 1150 else "card-long"
        self.card_length = "card"
    
    def __str__(self):
        fout = f"<div class='cards-container'>\n"
        fout+= f"    <div class='{self.card_length}'>\n"
        fout+= f"        <div class='item_name'><h1>\n"
        fout+= f"            {self.item_name}\n"
        fout+= f"        </h1></div>\n"
        fout+= f"        <div class='top-section'>\n"
        fout+= f"            {self.item_type}\n"
        fout+= f"        </div>\n"
        fout+= f"        <div class='section'>\n"
        fout+= f"            <span class='subtitle'>Source:</span>\n"
        fout+= f"            <span class='desc'>{self.source}</span>\n"
        fout+= f"        </div>\n"
        sout = ""
        if self.storage!="-":
            sout+= f"        <div class='section'>\n"
            sout+= f"            <span class='subtitle'>Store in:</span>\n"
            sout+= f"            <span class='short-desc'>{self.storage}</span>\n"
            sout+= f"        </div>\n"
        if self.ingredient_type!="-":
            sout+= f"        <div class='section'>\n"
            sout+= f"            <span class='subtitle'>Use as ingredient for:</span>\n"
            sout+= f"            <span class='short-desc'>{self.ingredient_type}</span>\n"
            sout+= f"        </div>\n"
        if self.crafting_value!="-":
            sout+= f"        <div class='section'>\n"
            sout+= f"            <span class='subtitle'>Crafting Value (when used as ingredient):</span>\n"
            sout+= f"            <span class='short-desc'>{self.crafting_value}</span>\n"
            sout+= f"        </div>\n"
        if self.use!="-":
            sout+= f"        <div class='section'>\n"
            sout+= f"            <span class='subtitle'>Use:</span>\n"
            sout+= f"            <span class='short-desc'>{self.use}</span>\n"
            sout+= f"        </div>\n"
        if self.description != "-":
            sout+= f"        <div class='section'>\n"
            sout+= f"            <span class='subtitle'>Description:</span>\n"
            sout+= f"            <span class='desc'>{self.description}</span>\n"
            sout+= f"        </div>\n"
        if self.cooking_effect != "-":
            sout+= f"        <div class= 'divider'></div>\n"
            sout+= f"        <div class='section'>\n"
            sout+= f"            <span class='subtitle'>Cooking Effect:</span>\n"
            sout+= f"            <span class='desc'>{self.cooking_effect}</span>\n"
            sout+= f"        </div>\n"
        # 33 lines before break, avg 50 chars per line
        lines = (
            (len(sout)//51)
            -(sout.count("<span class='subtitle'>")*2)
            +(sout.count("<br>"))
            # +(sout.count("<div class= 'divider'>"))
            )
        out = fout+sout
        if lines > 30:
            print(f"Warning: card text too long for card {self.item_name}, using two cards *counted {lines} lines.")
            out+= f"    </div>\n"
            out+= f"    <div class='{self.card_length}'>\n"
            out+= f"        <div class='item_name'><h1>\n"
            out+= f"            {self.item_name}\n"
            out+= f"        </h1></div>\n"
            out+= f"        <div class='top-section'>\n"
            out+= f"            Continued (2)\n"
            out+= f"        </div>\n"
        out+= f"    </div>\n"
        out+= f"</div>\n"
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