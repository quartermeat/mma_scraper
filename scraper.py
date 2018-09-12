import requests
import re
from bs4 import BeautifulSoup

def get_soup(current_page):
    page = requests.get(current_page)
    soup = BeautifulSoup(page.content)
    return soup

# get_fighter_links takes raw_links and adds /fighter links to the existing list
# from the given page
# param raw_links   : a href links grabbed from get_raw_links
def get_fighter_links(raw_links, fighters):
    urlroot = "https://www.mixedmartialarts.com/"
    # pattern = re.compile(r'<a href=\"\/*fighter\/[A-Za-z]*-[A-Za-z]*:[A-Z0-9]*\">')
    pattern = re.compile(r'\/?fighter\/[A-Za-z]*-[A-Za-z]*:[A-Z0-9]*')
    for line in raw_links:
        match = re.search(pattern, line)
        if match:
            fighter = urlroot + match.group(0)
            if fighter not in fighters:
                fighters.append(fighter)

    return fighters

#get_raw_links but also call get_fighter_links to process them, before returning processed list
def get_complete_links(pages, fighters):
    return_list = []
    raw_links = []
    #we need to limit this to pages we have not yet visited
    for page in pages:
        print("getting links from page : " + str(page))
        soup = get_soup(page)
        list_of_link_lines = soup.find_all('a')
        for line in list_of_link_lines:
            raw_links.append(line.prettify())

    return get_fighter_links(raw_links, fighters)

# writes any fighters in second_list that aren't in first_list
def write_new_fighters(new_fighters, fighters):
    new_fighters_written = []

    for fighter in new_fighters:
         if fighter not in fighters:
             #write new link to file
             with open("C:/Users/jerem/Documents/sherdog_scraper/fighter_links.txt", 'a', encoding='utf8') as file:
                 print("writing : " + fighter)
                 file.write(fighter + '\n')
                 new_fighters_written.append(fighter)

    return new_fighters_written

def get_cached_links():
    fighter_file = "C:/Users/jerem/Documents/sherdog_scraper/fighter_links.txt"
    fighter_links = open(fighter_file, 'r').read().splitlines()
    return fighter_links

def main():
    #used to oop, so passing around fighters to maintain state, seems weird
    #maybe convert to class

    #setup content file
    rootpage = ["https://www.mixedmartialarts.com/fighter"]
    fighters = []
    new_fighters = get_complete_links(rootpage, fighters)
    write_new_fighters(new_fighters, fighters)
    fighters = fighters + new_fighters

    #do magic, assuming there are new fighters among the last 350
    while new_fighters:
        new_fighters = get_complete_links(new_fighters, fighters)
        write_new_fighters(new_fighters, fighters)
        fighters = fighters + new_fighters

    print("Done scraping!\n")

if __name__ == "__main__":
    main()
