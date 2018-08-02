"""
Web scrapes the comic website and creates a pdf version of it.
"""
import urllib.request as urllib2
import http
import os
import sys

from bs4 import BeautifulSoup
from fpdf import FPDF

# Archive of Comics | Nineteen Letters Long
COMIC_URL = "http://nineteenletterslong.com/take-me-to-the/archive/"

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
    
    a_tags = soup.find("div", attrs={"class":"archive"}).find_all("a")
    pg_no, idx = 1, 1
    for a_tag in a_tags:
        comic_img_url = "http://nineteenletterslong.com" + a_tag['href']
        soup = get_soup(comic_img_url)
        if soup == -1:
            continue
        
        for img in soup.find_all("img", attrs={"class":"comic"}):
            img_url = "http://nineteenletterslong.com" + img['src']
            img_name = os.path.join(IMAGE_REPOSITORY, "ntll{}.{}".format(idx, img_url[-3:]))
            OPENER.retrieve(img_url, img_name)
            pdf.add_page()
            pdf.image(img_name, 0, 0, 210, 297)
            idx += 1
            
        print("Page no: {}".format(pg_no))   
        pg_no += 1

def main():
    """
    Entry-point for the function.
    """
    pdf = FPDF()
    pdf.set_display_mode('fullwidth')
    pdf.set_creator('Cavin Dsouza')
    pdf.set_author('nineteenletterslong')
    scrape(COMIC_URL, pdf)
    print("Creating PDF file...")
    pdf.output("nineteen_letters_long.pdf", "F")
    print("PDF created successfully.") 
    
if __name__ == "__main__":
    main()
    
