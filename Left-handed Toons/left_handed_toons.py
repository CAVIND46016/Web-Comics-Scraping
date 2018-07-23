"""
Web scrapes the comic website and creates a pdf version of it.
"""
import urllib.request as urllib2
import http
import sys
import os

from bs4 import BeautifulSoup
from fpdf import FPDF

sys.setrecursionlimit(3000)
# Left-Handed Toons (by right-handed people)!
COMIC_URL = "http://www.lefthandedtoons.com/"

DIRNAME = os.path.dirname(__file__)
IMAGE_REPOSITORY = os.path.join(DIRNAME, 'images')

def scrape(web_url, pdf, pg_no):
    """
    Web scraping logic
    """
    try:
        page = urllib2.urlopen(web_url, timeout=200)
    except http.client.RemoteDisconnected:
        print("Error 404: {} not found.".format(web_url))
        return 0
    
    soup = BeautifulSoup(page, "html.parser")
    div_id_main = soup.find("div", attrs={"id":"main"})
    div_class_comic_data = div_id_main.find("div", attrs={"class":"comicdata"})
    comic_image = div_class_comic_data.find("img", attrs={"class":"comicimage"})
    gif_name = os.path.join(IMAGE_REPOSITORY, "lht{}.gif".format(pg_no))
    urllib2.urlretrieve(comic_image['src'], gif_name)
    pdf.add_page()
    pdf.image(gif_name, 0, 0, 210, 297)

    li_class_prev = div_id_main.find("li", attrs={"class":"prev"})
    if not li_class_prev:
        return 0
    
    prev_page_href = li_class_prev.find("a")
    # Construct next page url.
    prev_page_url = "{}{}".format(COMIC_URL, prev_page_href['href'])
    print("Page no: {}".format(pg_no))
    pg_no += 1

    # recursive logic
    scrape(prev_page_url, pdf, pg_no)

def main():
    """
    Entry-point for the function.
    """
    pdf = FPDF()
    pdf.set_display_mode('fullwidth')
    pdf.set_creator('Cavin Dsouza')
    pdf.set_author('lefthandtoons')
    scrape(COMIC_URL, pdf, pg_no=1)
    pdf.output("left_handed_toons.pdf", "F")
    print("PDF created successfully.") 
    
if __name__ == "__main__":
    main()
    
