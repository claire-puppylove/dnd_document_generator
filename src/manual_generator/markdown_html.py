# -*- encoding: UTF-8 -*-
"""Markdown Preview main."""
import os
import codecs
from markdown import Markdown
from markdown.extensions.tables import TableExtension

# references: https://github.com/facelessuser/MarkdownPreview/blob/master/markdown_preview.py

def load_utf8(filename):
    """Load UTF8 file."""
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return f.read()

class MarkdownCompiler:
    """Python Markdown compiler."""
    compiler_name = "markdown"
    default_css = [
        "./css/markdown.css",
        "./css/libre-baskerville.css",
        "./css/noto-sans.css",
        "./css/dnd.min.css",
        "./css/dnd_like.css",
        # "./css/statblock-style.css",
        ]
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
    def get_default_css(self):
        """Locate the correct CSS with the `css` setting."""
        css_text = []
        css_text = [
            f"<style>{load_utf8(os.path.expanduser(i))}</style>"
            for i in self.default_css
            ]
        return '\n'.join(css_text)
    def convert_markdown(self, markdown_text):
        """Convert input markdown to HTML, with GitHub, GitLab or builtin parser."""
        md = Markdown(extensions=[TableExtension(use_align_attribute=True)])
        markdown_html = md.convert(markdown_text)
        return markdown_html
    def run(self, markdown_text, title):
        """Return full HTML and body HTML for view."""
        contents = markdown_text
        body = self.convert_markdown(contents)
        html = '<!DOCTYPE html>'
        html += '<html><head><meta charset="utf-8">'
        html += '<meta name="viewport" content="width=device-width, initial-scale=1">'
        html += self.get_default_css()
        html += '<title>%s</title>' % title
        html += '</head><body>'
        html += '<article class="markdown-body">'
        html += body
        html += '</article>'
        html += '</body>'
        html += '</html>'
        return html, body

