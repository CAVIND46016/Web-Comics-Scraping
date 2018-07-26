"""
Web scrapes the comic website and creates a pdf version of it.
"""
import urllib.request as urllib2
import http
import os
import sys

from bs4 import BeautifulSoup
from fpdf import FPDF

# Comic Archives - Channelate
COMIC_URL = "http://www.channelate.com/comic-archives/"

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
    
def scrape(web_url, pdf):
    """
    Web scraping logic
    """
    soup = get_soup(web_url)
    if soup == -1:
        sys.exit(0)
        
    div_class_entry = soup.find("div", attrs={"class":"entry"})
    archives = div_class_entry.find_all("td", attrs={"class":"archive-title"})
    pg_no = 1
    for archive in archives:
        web_url = archive.find("a")['href']
        soup = get_soup(web_url)
        if soup == -1:
            print(web_url)
            continue

        div_id_comic = soup.find("div", attrs={"id":"comic"})
        comic_image = div_id_comic.find("img")
        if not comic_image:
            print(web_url)
            continue
        
        img_url = comic_image['src']
        img_name = os.path.join(IMAGE_REPOSITORY, "chan{}.{}".format(pg_no, img_url[-3:]))
        OPENER.retrieve(comic_image['src'], img_name)
        pdf.add_page()
        pdf.image(img_name, 0, 0, 210, 297)
        print("Page no: {}".format(pg_no))
        pg_no += 1

def main():
    """
    Entry-point for the function.
    """
    pdf = FPDF()
    pdf.set_display_mode('fullwidth')
    pdf.set_creator('Cavin Dsouza')
    pdf.set_author('channelate')
    scrape(COMIC_URL, pdf)
    print("Creating PDF file...")
    pdf.output("channelate.pdf", "F")
    print("PDF created successfully.") 
    
if __name__ == "__main__":
    main()
    
