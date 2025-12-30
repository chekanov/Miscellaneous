# Retrive ANL-HEP papers from aXiv

import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# should include an author?
isFilter=False   


# Define the search URL
base_url = 'http://export.arxiv.org/api/query?'
query = 'search_query=all:ANL-HEP&start=0&max_results=700&sortBy=submittedDate&sortOrder=descending' # Example query
url = base_url + query

# Perform the HTTP request and read the response
response = urllib.request.urlopen(url).read()
xml_data = response.decode('utf-8')

# Define the Atom namespace
# This is crucial for finding elements correctly in the Atom feed
NS = {'atom': 'http://www.w3.org/2005/Atom'}

# Parse the XML data
root = ET.fromstring(xml_data)

# Find all paper entries
entries = root.findall('atom:entry', NS)

# keep counts
dcount={}


for entry in entries:
    title = entry.find('atom:title', NS).text.strip()
    print(f"Title: {title}")
    
    # Find all authors within the entry
    authors = entry.findall('atom:author', NS)
    author_names = [author.find('atom:name', NS).text for author in authors]
    id_element = entry.find('atom:id', NS)
    id_published = entry.find('atom:published', NS)
    summary = entry.find('atom:summary', NS).text
    published = entry.find('atom:published', NS).text

    if (isFilter):
       s=""
       for n in author_names:
         s=s+" "+str(n) 
       if (s.find("Chekanov")>-1): continue 


    print(f"Time: {published}")
    print(f"Authors: {', '.join(author_names)}")
    print("-" * 20)
    dt_object = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
    year = dt_object.year

    if year in dcount: dcount[year]=dcount[year]+1
    else: dcount[year]=1


# Calculate the sum of all values
total_sum = sum(dcount.values())
print("Total number of articles=",total_sum)

import matplotlib.pyplot as plt

# Split the dictionary into keys (years) and values (counts)
years = list(dcount.keys())
counts = list(dcount.values())

# Create the plot
plt.figure(figsize=(10, 6)) # Optional: adjust figure size
plt.bar(years, counts, color='skyblue') # Use plt.bar for a bar chart, or plt.plot for a line chart

# Add labels and title
plt.xlabel("Year")
plt.ylabel("Count")
plt.title("Nr of aXiv submissions per Year from ANL-HEP")

# Ensure years are treated as discrete values and labels are readable
plt.xticks(years, rotation=45) # Rotate labels for better readability

# Display the plot
plt.show()
