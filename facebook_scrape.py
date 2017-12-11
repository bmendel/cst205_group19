###########################################################
# Filename: facebook_scrape.py
# Author: Rob Mann
# Course: CST 205
# Last Updated: 12/10/17
#
# Uses web scraping to find facebook profile pictures
###########################################################

from bs4 import BeautifulSoup
import urllib.request as urlrequest
from PIL import Image

# Retrieves a profile image from facebook given a url,
# and saves said image to the directory the application is in
def scrape_profile(url, image):
	websiteCode = urlrequest.urlopen(url).read()
	soup = BeautifulSoup(websiteCode, 'html.parser')
	urlrequest.urlretrieve(soup.findAll('img')[3].attrs['src'], image)