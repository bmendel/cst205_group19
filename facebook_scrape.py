from bs4 import BeautifulSoup
import urllib.request as urlrequest
from PIL import Image

def scrape_profile(url, image):
	websiteCode = urlrequest.urlopen(url).read()
	soup = BeautifulSoup(websiteCode, 'html.parser')
	urlrequest.urlretrieve(soup.findAll('img')[3].attrs['src'], image)