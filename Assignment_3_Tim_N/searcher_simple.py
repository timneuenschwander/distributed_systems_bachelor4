import csv
from bs4 import BeautifulSoup
import time

"""
Task 3.1
"""

#definitions
word = input("Enter a word ")
b = []

start = time.time()
with open("Assignment3_records.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if word in row:
            b.append(row[0])

b = str(b)[1:-1]
print("Word found on following pages:", b)
end = time.time()
print(f"Runtime of the program is {end - start}")

