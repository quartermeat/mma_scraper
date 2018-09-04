import requests
import re
from bs4 import BeautifulSoup

def get_soup(current_page):
    page = requests.get(current_page)
    soup = BeautifulSoup(page.content)
    return soup

root_page = "https://www.mixedmartialarts.com/fighter"

#for testing
def setup_root_page(current_page, file_name):
    soup = get_soup(current_page)
    with open(file_name, "w", encoding="utf8") as file:
        list_of_link_lines = soup.find_all('a')
        for line in list_of_link_lines:
            file.write(line.prettify())

def get_fighter_links(file_name):
    pattern = re.compile(r'<a href=\"\/*fighter\/[A-Za-z]*-[A-Za-z]*:[A-Z0-9]*\">')
    links = []
    with open(file_name, 'r', encoding='utf8') as file:
        for line in file:
            match = re.search(pattern, line)
            if match and match.group(0) not in links:
                links.append(match.group(0))
    return links

def main():
    #setup content file
    file_name = "output.html"
    setup_root_page(root_page, file_name)
    fighter_links = get_fighter_links(file_name)
    for fighter in fighter_links:
        print(fighter)

if __name__ == "__main__":
    main()
