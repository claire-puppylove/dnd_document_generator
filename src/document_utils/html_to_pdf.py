import re
import textwrap
from typing import Literal

## HTML to PDF Options

# WeasyPrint
import weasyprint
from weasyprint.text.fonts import FontConfiguration
# no browser dependency
# does not respect overflow to continued cards.

# pyhtml2pdf
import pyhtml2pdf.converter
# most successful for my project until now, but...
# has chromedriver dependency (separate install, problem for de-googled users AND less experienced users)
# has ghostscirpt dependency (separate install, problem for less experienced users)


# playwright 
# depends on browsers still
from playwright.sync_api import sync_playwright

# pdfkit 
import pdfkit
# has hard to install wkhtmltopdf dependency


def html_to_pdf(
        html_content,
        output_path,
        pdf_backend:Literal[
            'weasyprint',
            'pyhtml2pdf',
            'playwright-firefox',
            'playwright-chromium',
            'pdfkit',
            ]='weasyprint',
        ):
    # PDF render
    if pdf_backend == "weasyprint":
        font_config = FontConfiguration()
        matches = re.findall(
            r'<style>((.|\n)*)^</style>',
            html_content,
            flags=re.MULTILINE)
        if len(matches)>0:
            css = [weasyprint.CSS(string=match[0], font_config=font_config) for match in matches]
        else:
            css = []
        whtml = weasyprint.HTML(string=html_content)
        whtml.write_pdf(output_path, stylesheets=css, font_config=font_config)

    if pdf_backend == "pyhtml2pdf":
        pyhtml2pdf.converter.convert(
            source=html_content,
            target=output_path,
            # print_options={
            #     "marginBottom":0.4,
            #     "marginTop":0.4,
            #     "marginLeft":0,
            #     "marginRight":0,
            #     "printBackground":False,
            # }
        )

    if pdf_backend == "playwright-firefox":
        with sync_playwright() as p:
            browser = p.firefox.launch()
            page = browser.new_page()
            page.set_content(html_content)
            page.pdf(path=output_path)
            browser.close()

    if pdf_backend == "playwright-chromium":
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_content(html_content)
            page.pdf(path=output_path)
            browser.close()
    