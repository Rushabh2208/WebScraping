from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json
import re

myUrl = 'https://www.yellowpages.com/search?search_terms=coffee&geo_location_terms=Los+Angeles%2C+CA'
uClient = uReq(myUrl)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

filename = "products1.csv"
f = open(filename, "w")
headers = "Name, Rating, Address, Contact no., Review"
f.write(headers)

for i in range(1, 50):
    print("Scraping Page "+str(i)+" ..........")
    nextLink = "https://www.yellowpages.com/search?search_terms=Coffee&geo_location_terms=Los%20Angeles%2C%20CA&page=" + str(i)
    uClient = uReq(nextLink)
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.findAll("div", {"class": "info"})

    for container in containers:
        link = container.h2.a['href']
        inLink = "https://www.yellowpages.com"+str(link)
        uClient1 = uReq(inLink)
        inLinkContent = uClient1.read()
        page_soup = soup(inLinkContent, "html.parser")

        name = container.h2.a.text
        try:
            ratObj = json.loads(container.div["data-tripadvisor"])
            rating = ratObj["rating"]

        except:
            rating = " "

        try:
            contact_no = container.div.find("div", {"class": "phones phone primary"}).text
        except:
            contact_no = " "

        try:
            review = page_soup.find("div", {"class": "review-response"}).text

        except:
            review = " "

        address = container.div.p.text

        f.write("\n" + name.replace(",", " ") + "," + rating + "," + address.replace(",", " ") + "," + contact_no + "," + review.replace(","," "))
    print("Page " + str(i) + " Scraped ...........")
f.close
