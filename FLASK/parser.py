import re
import urllib2
from bs4 import BeautifulSoup

link = 'https://www.youtube.com/watch?v=7hlGqj3ImQI'

html = urllib2.urlopen(link)

soup = BeautifulSoup(html, 'html.parser')

firstElement = soup.find('span', text = re.compile(r'H. TRIBUNAL SUPERIOR'))

print firstElement