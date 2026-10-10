import re
import textwrap
from pyhtml2pdf import converter # chromedriver, ghostscirpt dependency

# import pdfkit # wkhtmltopdf dependency
# import weasyprint # errors
# import asyncio
# from playwright.async_api import async_playwright
# async def html_to_pdf(html_content, output_path):
#     async with async_playwright() as p:
#         browser = await p.firefox.launch()
#         page = await browser.new_page()
#         await page.set_content(html_content)
#         await page.pdf(path=output_path)
#         await browser.close()

def html_to_pdf(html_content, output_path):
    # regex extract media print and add as normal CSS
    # @media print {((.|\n)*)^}
    match = re.search(
        r'@media print {((.|\n)*)^}',
        html_content,
        flags=re.MULTILINE)
    if match:
        media_print_css = match.group(0) # the entire match
        css_insert = media_print_css[len("@media print {\n")+1:-3]
        css_insert = textwrap.dedent(css_insert)
        insert_index = html_content.find("</style>")
        html_content = html_content[:insert_index] + css_insert + html_content[insert_index:]
    converter.convert(
        source=html_content,
        target=output_path,
        print_options={
            "marginBottom":0.4,
            "marginTop":0.4,
            "marginLeft":0,
            "marginRight":0,
            "printBackground":False,
        }
    )