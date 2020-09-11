import requests
import json
import time

# https://www.ratemyprofessors.com/filter/professor/?&page=1&queryoption=TEACHER&queryBy=schoolId&sid=727
# 132 pages of data 10sec crawl time = 22 hours.
# # Since this will only need to fetch data at max 4 times a year might slow that down more


# Rate my professor scraper
# Scrapes all professors names & scores
# Sends to server
# robots.txt states crawl time of 10 secconds



class RMP:
  def __init__(self, school_id, crawl_time=10):
    self.school_id = school_id
    self.robots_info = ['']
    self.crawl_time = crawl_time

  def scrape_scores(self):
    page_num = 1
    keepGoing = True
    while (keepGoing):
      read_page(page_num)
      page_num += 1


  def read_page(self, n):
    link = 'https://www.ratemyprofessors.com/filter/professor/?&page={}&queryoption=TEACHER&queryBy=schoolId&sid={}'.format(n,self.school_id)
    page = requests.get(link)
    data = json.loads(page.content)
    print(data)


  def crawl_delay(self):
    time.sleep(crawl_time)







###
if __name__ == '__main__':
  rmp = RMP(727)
  rmp.read_page(1)