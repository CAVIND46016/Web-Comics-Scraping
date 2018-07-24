"""
Web scrapes the comic website and creates a pdf version of it.
"""
import urllib.request as urllib2
import http
import time
import os

from bs4 import BeautifulSoup
from fpdf import FPDF

# Completely Serious Comics
COMIC_URL = "http://completelyseriouscomics.com/"

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
    div_id_comic = soup.find("div", attrs={"id":"comic"})
    comic_image = div_id_comic.find("img")
    img_name = os.path.join(IMAGE_REPOSITORY, "csc{}.jpg".format(pg_no))
    urllib2.urlretrieve(comic_image['src'], img_name)
    pdf.add_page()
    pdf.image(img_name, 0, 0, 210, 297)

    td_class_prev= soup.find("td", attrs={"class":"comic_navi_left"})
    a_tags = td_class_prev.find_all("a")
    if len(a_tags) == 0:
        return 0
    
    # Construct next page url.
    prev_page_url = a_tags[-1]['href']
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
    pdf.set_author('completelyseriouscomics')
    scrape(COMIC_URL, pdf, pg_no=1)
    pdf.output("completely_serious_comics.pdf", "F")
    print("PDF created successfully.") 
    
if __name__ == "__main__":
    main()
    
