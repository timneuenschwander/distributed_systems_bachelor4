import csv
from bs4 import BeautifulSoup


"""
Task 3.2
"""

#definitions

# Creating an empty dictionary
myDict = {}
mylist = []

with open("Assignment3_records.csv") as csvfile:
    reader = csv.reader(csvfile)
    index = list(reader)
    print(index)
    print("")


for list in index:
    for term in list[1:]:  
        if term not in myDict:
            myDict[term] = []
            myDict[term].append(list[0])
        else:
            myDict[term].append(list[0])

print(myDict)



# name of csv file 
filename = "Assignment3_records2.csv"
    
# writing to csv file 
with open(filename, "w", newline="") as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)  
    for key in myDict:
        csvwriter.writerow([key,*myDict[key]])









    
    
    
    
    
    
    