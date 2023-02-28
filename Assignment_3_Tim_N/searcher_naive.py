import requests
import re
from bs4 import BeautifulSoup


"""
Task 1
"""
#definitions
checked_links = []
successfull_links = []
all_page = []

word = input("Enter a word ")

url_base = "https://api.interactions.ics.unisg.ch/hypermedia-environment/"
url_det = "cc2247b79ac48af0"

#methods
def find_links(contents):
    soup = BeautifulSoup(contents.text, 'html.parser')
    links_list = soup.body.find_all('a')
    for i in links_list:
        if 'href' in i.attrs and str(i.attrs['href']) not in all_page:
            all_page.append(str(i.attrs['href']))

def find_word(contents):            
    soup = BeautifulSoup(contents.text, 'html.parser')
    word_list = soup.body.find_all('p')
    results1 = soup.body.find_all(string=re.compile('.*{0}.*'.format(word)), recursive=True)
    if len(results1) > 0:
        successfull_links.append(url_det)
        print('Found the word "{0}" {1} times in {2}'.format(word, len(results1), (url_base + i)))
    else:
        print('Found the word "{0}" {1} times in {2}'.format(word, len(results1), (url_base + i)))
        print("The size of the hypermedia environment is:", len(all_page))

#initiate 1. object
all_page.append(url_det)

#Loop for all Web Pages
for i in all_page:
    if i not in checked_links:
        contents = requests.get(url_base + i)
        find_links(contents)
        find_word(contents)
        checked_links.append(i)
    if len(all_page) == 100:
        break