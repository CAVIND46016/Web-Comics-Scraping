"""
Web scrapes the comic website and creates a pdf version of it.
"""
import urllib.request as urllib2
import http
import os
import datetime
import csv

from bs4 import BeautifulSoup
from fpdf import FPDF

# Cyanide & Happiness (Explosm.net)
COMIC_URL = "http://explosm.net/comics/{}/"

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
    except :
        print("Error 404: {} not found.".format(web_url))
        return -1
    
    return BeautifulSoup(page, "html.parser")
    
def scrape(comic_url, pdf):
    """
    Web scraping logic
    """
    start_page, img_num = 15, 1
    print("Writing comic source links...")
    while True:
        web_url = comic_url.format(start_page)
        print(web_url)
        soup = get_soup(web_url)
        if soup == -1:
            start_page += 1
            continue
            
        comic_image = soup.find("img", attrs={"id":"main-comic"})
        image_url = "http:" + comic_image['src']
        print(image_url)
        img_name = os.path.join(IMAGE_REPOSITORY, "explosm_{}.{}".format(img_num, image_url[-3:]))
        OPENER.retrieve(image_url, img_name)
        pdf.add_page()
        pdf.image(img_name, 5, 5, 200, 75)
        print("Page no: {}".format(start_page))
        start_page += 1
        img_num += 1
        

def main():
    """
    Entry-point for the function.
    """
    pdf = FPDF()
    pdf.set_display_mode('fullwidth')
    pdf.set_creator('Cavin Dsouza')
    pdf.set_author('explosm')
    scrape(COMIC_URL, pdf)
    print("Creating PDF file...")
    pdf.output("explosm.pdf", "F")
    print("PDF created successfully.") 
    
if __name__ == "__main__":
    main()
    
