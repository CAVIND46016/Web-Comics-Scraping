"""
Web scrapes the comic website and creates a pdf version of it.
"""
import urllib.request as urllib2
import http
import sys
import os
import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fpdf import FPDF

sys.setrecursionlimit(10**5)

# Bizarro - Daily Comic
COMIC_URL = "https://bizarro.com/daily-comic/"
# COMIC_START_DATE >= 1996-02-04
COMIC_START_DATE = datetime.date(2018, 7, 15)
COMIC_END_DATE = datetime.datetime.now().date()

DIRNAME = os.path.dirname(__file__)
IMAGE_REPOSITORY = os.path.join(DIRNAME, 'images')

# Fixing the 'IncompleteRead' bug using http
# https://stackoverflow.com/questions/14149100/incompleteread-using-httplib
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

# firefox browser object
BROWSER = webdriver.Firefox()

def scrape(pdf):
    """
    Web scraping logic
    """
    date_ = COMIC_START_DATE
    idx = 1
    while date_ <= COMIC_END_DATE:
        web_url = "{}?fd={}".format(COMIC_URL, date_)
        try:
            BROWSER.set_page_load_timeout(200)
            BROWSER.get(web_url)
        except http.client.RemoteDisconnected:
            print("Error 404: {} not found.".format(web_url))
            return 0
        
        WebDriverWait(BROWSER, 200).until(EC.presence_of_element_located\
                                            ((By.ID, "kfs-comic")))
        
        soup = BeautifulSoup(BROWSER.page_source, "html.parser")
        comic_image = soup.find("img", attrs={"id":"kfs-comic"})
        img_name = os.path.join(IMAGE_REPOSITORY, "biz{}.png".format(idx))
        urllib2.urlretrieve(comic_image['src'], img_name)
        pdf.add_page()
        pdf.image(img_name, 0, 0, 210, 297)
        print("Page no: {} - {}".format(idx, date_))
        date_ += datetime.timedelta(days=1)
        idx += 1
    
    BROWSER.quit()

def main():
    """
    Entry-point for the function.
    """
    pdf = FPDF()
    pdf.set_display_mode('fullwidth')
    pdf.set_creator('Cavin Dsouza')
    pdf.set_author('bizarro')
    scrape(pdf)   
    pdf.output("bizarro.pdf", "F")
    print("PDF created successfully.") 
    
if __name__ == "__main__":
    main()
    
