import requests
import re
from bs4 import BeautifulSoup

def get_soup(current_page):
    page = requests.get(current_page)
    soup = BeautifulSoup(page.content)
    return soup

root_page = "https://www.mixedmartialarts.com/fighter"

#for testing
def setup_root_page(current_page):
    soup = get_soup(current_page)
    list_of_link_lines = soup.find_all('a')
    for line in list_of_link_lines:
        yield line.prettify()

def get_fighter_links(raw_links, links):
    # pattern = re.compile(r'<a href=\"\/*fighter\/[A-Za-z]*-[A-Za-z]*:[A-Z0-9]*\">')
    pattern = re.compile(r'\/?fighter\/[A-Za-z]*-[A-Za-z]*:[A-Z0-9]*')
    for line in raw_links:
        match = re.search(pattern, line)
        if match and match.group(0) not in links:
            links.append(match.group(0))

    return links

def main():
    #setup content file
    url = "https://www.mixedmartialarts.com/"
    # just the a href link
    links = []
    # the fully formed url from links
    url_list = []
    fighter_links = get_fighter_links(setup_root_page(root_page), links)
    for fighter in fighter_links:
        url_list.append(url + fighter)

    for link in url_list:
        print(link)

if __name__ == "__main__":
    main()
