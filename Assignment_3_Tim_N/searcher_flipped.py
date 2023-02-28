import csv
from bs4 import BeautifulSoup
import time

"""
Task 3.3
"""

#definitions
word = input("Enter a word ")

start = time.time()
with open("Assignment3_records2.csv") as csvfile:
    reader = csv.reader(csvfile)
    index = list(reader)
    for list in index:
        if word in list:
            b = str(list[1:])[1:-1]
            print("Word found on following pages:", b)
end = time.time()
print(f"Runtime of the program is {end - start}")