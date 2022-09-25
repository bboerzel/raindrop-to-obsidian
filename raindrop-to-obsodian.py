"""
Raindrop to Obsidian
This is a little python script that helps me writing a weekly review blogpost of what happened the last week. 
Over the week I collect blogposts in Raindrop.IO, this script grabs all the saved blogposts from one specified collection 
and exports it to a markdown file, sorted by tags, in my Obsidian vault. 
This script is only tested on a MAC! 

Source: https://github.com/bboerzel/raindrop-to-obsidian

Author: Benjamin Börzel 
Twitter: @boerzel
version: 0.1
last change: 2022.09.25

Changelog
v0.1
 Initial Script
"""


# library imports
from typing import Collection
from raindropio import API, CollectionRef, Raindrop
import datetime, os

# settings, please change values as needed
api = API("ENTER-API-LKEY")   #Raindrop API Key
collection_id = 12345    # Raindrop Collection ID where the Blogposts are
obsidian_blogpost_folder ="/Users/demouser/documents/obsidian/blog/" # Folder where the blogposts should get stored to
obsidian_vault = "obsidian" # Your obsidian vault name

# initial variables
page = 0
my_date = datetime.date.today()
year, week_num, day_of_week = my_date.isocalendar()
kw = str(year)+"KW"+str(week_num)
blogtitle = "blogpost_"+kw
blogfile = obsidian_blogpost_folder+blogtitle+".md"

with open(blogfile, "w") as file:   # Open new file
    
    # getting tags is not yet implemented or (could not find out) in python-raindropip lib so we get it ourselfs.
    params = {} # no parameter needed
    URL = f"https://api.raindrop.io/rest/v1/tags/{collection_id}" # api url to collect the tags
    results = api.get(URL, params=params).json()    # get our tags
    
    print("[+] Getting Bookmarks")
    for collection_tags in results["items"]:    # fo through all tags one by one
        print(collection_tags['_id'])
        file.write("\n# "+collection_tags['_id']+"\n")  # write tag as title / header 1
        while (items:=Raindrop.search(api, collection=CollectionRef({"$id": collection_id}), page=page)): # get all blogposts from the raindrop collection page by page
            for item in items: # go through the list of posts one by one
                if collection_tags['_id'] in item.tags : # check if the header tag is in the blogpost
                    print("  - "+item.title)                                
                    file.write("- ["+item.title+"]("+item.link+")\n") # write blog title and url as link
            page += 1 # get next page
        page = 0 # when there are no more pages / blogpost for that tag, reset pages to 0 ang go to next tag

print("\n[+] Raindrop.io Bookmarks exported to: "+blogfile)

obsidian_file= f"obsidian://open?vault={obsidian_vault}&file={blogtitle}" #construct the obsidian url
print("[+] open \""+obsidian_file+"\"")
os.system("open \""+obsidian_file+"\"") # finally open obsidian with our newly created blogpost file
