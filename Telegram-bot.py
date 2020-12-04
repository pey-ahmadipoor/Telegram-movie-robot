from bs4 import BeautifulSoup
from telegram.ext import Updater
from telegram.ext import CommandHandler
import requests
import re
import time


class SiteVideos:
    def __init__(self):
        pass

    @staticmethod
    def request(url):
        return requests.get(url=url)

    def parser(self, url):
        return BeautifulSoup(self.request(url).content, 'html.parser')

    def get_posters(self, url):
        soup = self.parser(url)
        find_all_tag = soup.find_all('img', {'class': 'attachment-thumb-207-290 size-thumb-207-290 wp-post-image'})
        list_posters = []
        for image in find_all_tag:
            list_posters.append(image['src'])
        return list_posters

    def get_names(self, url):
        soup = self.parser(url)
        find_all_tag = soup.find_all('div', {'class', 'content'})
        # Because the last index of the find_all_tag list is the footer of the site and there is no tag in the
        # footer called h1, the program gets an error, so we delete the last index of the list so that the program
        # does not get an error.
        find_all_tag.pop(-1)
        list_names = []
        for i in find_all_tag:
            # find_all_tag[2].find('h1').find('a').contents
            list_names.append(i.find('h1').find('a').contents)
        s = ''.join(str(e) for e in list_names)
        patt = r'[A-Z]+[a-zA-Z \:\.\,\d]+'
        # Separate Persian words from English words and add to list
        list_names = re.findall(patt, s)
        return list_names
    
    def get_rates(self, url):
        soup = self.parser(url)
        find_all_tag = soup.find_all('div', {'class': 'info_bar'})
        list_rates = []
        for i in find_all_tag:
            list_rates.append(i.find_all('span', {'class': 'item'})[0].find('span').contents[0])
        return list_rates
    
    def get_dates(self, url):
        soup = self.parser(url)
        find_all_tag = soup.find_all('div', {'class': 'info_bar'})
        list_dates = []
        for i in find_all_tag:
            list_dates.append(i.find_all('span', {'class': 'item'})[1].contents[0])
        return list_dates
    
    def get_genre(self, url):
        soup = self.parser(url)
        find_all_tag = soup.find_all('div', {'class': 'info_bar'})
        list_genre = []
        list1 = []
        list2 = []
        count = 0
        for i in find_all_tag:
            list2.append(i.find_all('span', {'class': 'item'})[2].find_all('a'))
            for item in list2[count]:
                list1.append(item.contents[0])
            s = ', '.join(str(e) for e in list1)
            list1 = []
            list_genre.append(s)
            count += 1
            if count == 10:
                return list_genre
            
    def get_links(self, url):
        soup = self.parser(url)
        find_all_tag = soup.find_all('a', {'class': 'btn_dl'})
        list_links = []
        for i in find_all_tag:
            list_links.append(i['href'])
        return list_links

    def get_stories(self, url):
        list_stories = []
        for link in self.get_links(url):
            soup = self.parser(link)
            find_all_tag = soup.find('div', {'class': 'item_content'})
            list_stories.append(find_all_tag.findChildren()[-1].contents[0])
        return list_stories
