"""
Web scrapes the comic website and creates a pdf version of it.
"""
import urllib.request as urllib2
import http
import os
import datetime

from bs4 import BeautifulSoup
from fpdf import FPDF

# Dilbert by Scott Adams
COMIC_URL = "http://dilbert.com/strip/"

COMIC_START_DATE = datetime.date(1989, 4, 16)
COMIC_END_DATE = datetime.datetime.now().date()

DIRNAME = os.path.dirname(__file__)
IMAGE_REPOSITORY = os.path.join(DIRNAME, 'images')

REQUEST_HEADER = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                  (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}

OPENER = urllib2.URLopener()
OPENER.addheaders = [('User-Agent', REQUEST_HEADER['User-Agent'])]

def get_soup(web_url):
    try:
        req = urllib2.Request(web_url, headers=REQUEST_HEADER)
        page = urllib2.urlopen(req, timeout=200).read()
    except http.client.RemoteDisconnected:
        print("Error 404: {} not found.".format(web_url))
        return -1
    
    return BeautifulSoup(page, "html.parser")
    
def scrape(pdf):
    """
    Web scraping logic
    """
    _date = COMIC_START_DATE
    while _date <= COMIC_END_DATE:
        web_url = "{}{}".format(COMIC_URL, _date)
        soup = get_soup(web_url)
        if soup == -1:
            continue

        comic_image = soup.find("img", attrs={"class":"img-responsive img-comic"})
        img_name = os.path.join(IMAGE_REPOSITORY, "dilb_{}.gif".format(_date))
        urllib2.urlretrieve(comic_image['src'], img_name)
        pdf.add_page()
        pdf.image(img_name, 5, 5, 200, 75)
        print("Page no: {}".format(_date))
        _date += datetime.timedelta(days=1)

def main():
    """
    Entry-point for the function.
    """
    pdf = FPDF()
    pdf.set_display_mode('fullwidth')
    pdf.set_creator('Cavin Dsouza')
    pdf.set_author('dilbert')
    scrape(pdf)
    print("Creating PDF file...")
    pdf.output("dilbert.pdf", "F")
    print("PDF created successfully.") 
    
if __name__ == "__main__":
    main()
    
