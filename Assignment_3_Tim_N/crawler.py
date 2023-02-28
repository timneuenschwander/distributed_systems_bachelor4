import requests
import re
from bs4 import BeautifulSoup
import replace
import csv

"""
Task 2
"""

all_page = []
data_list = []

url_base = "https://api.interactions.ics.unisg.ch/hypermedia-environment/"
url_det = "cc2247b79ac48af0"

def find_links(url_det):
    data = requests.get(url_base + url_det)
    soup = BeautifulSoup(data.text, 'html.parser')
    links_list = soup.body.find_all('a')
    for i in links_list:
        if 'href' in i.attrs and str(i.attrs['href']) not in all_page:
            all_page.append(str(i.attrs['href']))

def find_word(url_det):            
    data = requests.get(url_base + url_det)
    soup = BeautifulSoup(data.text, 'html.parser')
    word_list = soup.body.find_all('p')
    words = []
    for i in word_list:
        words.append(i.getText())
    return(words)
       

all_page.append(url_det)

for i in all_page:
    find_links(i)
    if len(all_page) > 10:
            break

"""10 is for the control"""

for i in all_page:
    #print("This is the link:", (i), "These are the words:", (find_word(i)))
    #print("\n")
    #data_list.append(i)
    #data_list.append((("/" + i),(" ") + find_word(i)[0],(" ") + find_word(i)[1],(" ") + find_word(i)[2]))
    data_list.append((("/" + i),find_word(i)[0],find_word(i)[1],find_word(i)[2]))

#print(data_list)
# name of csv file 
filename = "Assignment3_records.csv"
    
# writing to csv file 
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)  
        
    # writing the data rows 
    csvwriter.writerows(data_list)

