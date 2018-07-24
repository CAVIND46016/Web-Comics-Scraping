"""
Web scrapes the comic website and creates a pdf version of it.
"""
import urllib.request as urllib2
import http
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fpdf import FPDF

# Cartoons Cartoons | Savage Chickens - Cartoons on Sticky Notes by Doug Savage
COMIC_URL = "http://www.savagechickens.com/category/cartoons"

DIRNAME = os.path.dirname(__file__)
IMAGE_REPOSITORY = os.path.join(DIRNAME, 'images')

# Fixing the 'IncompleteRead' bug using http
# https://stackoverflow.com/questions/14149100/incompleteread-using-httplib
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
# firefox browser object
BROWSER = webdriver.Firefox()

def scrape(web_url, pdf, idx, pg_no):
    """
    Web scraping logic
    """
    try:
        BROWSER.set_page_load_timeout(200)
        BROWSER.get(web_url)
    except http.client.RemoteDisconnected:
        print("Error 404: {} not found.".format(web_url))
        return 0
    
    WebDriverWait(BROWSER, 200).until(EC.presence_of_element_located\
                                        ((By.ID, "pagination")))
    
    soup = BeautifulSoup(BROWSER.page_source, "html.parser")
    div_class_entry_content = soup.find_all("div", attrs={"class":"entry_content"})
    for img_tag in div_class_entry_content:
        img_src = img_tag.find("img")['src']
        img_name = os.path.join(IMAGE_REPOSITORY, "sc{}.jpg".format(idx))
        urllib2.urlretrieve(img_src, img_name)
        pdf.add_page()
        pdf.image(img_name, 0, 0, 210, 297)
        idx += 1
        
    print("Page no: {}".format(pg_no))
    pg_no += 1
    span_class_prev_entry = soup.find("span", attrs={"class":"previous-entries"})
    if not span_class_prev_entry:
        return 0
    
    prev_page_url = span_class_prev_entry.find("a")['href']
    #Recursive logic
    scrape(prev_page_url, pdf, idx, pg_no)

def main():
    """
    Entry-point for the function.
    """
    pdf = FPDF()
    pdf.set_display_mode('fullwidth')
    pdf.set_creator('Cavin Dsouza')
    pdf.set_author('Savage Chickens')
    scrape(COMIC_URL, pdf, idx=1, pg_no=1)   
    BROWSER.quit()
    pdf.output("savage_chickens.pdf", "F")
    print("PDF created successfully.") 
    
if __name__ == "__main__":
    main()
    
