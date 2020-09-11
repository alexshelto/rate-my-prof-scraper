import requests
import json
import time

# pyt
# 132 pages of data 10sec crawl time = 22 hours.
# # Since this will only need to fetch data at max 4 times a year might slow that down more


# Rate my professor scraper
# Scrapes all professors names & scores
# Sends to server
# robots.txt states crawl time of 10 secconds

# https://www.ratemyprofessors.com/filter/professor/?&page=1&queryoption=TEACHER&queryBy=schoolId&sid=727

class RMP:
  def __init__(self, school_id, crawl_time=10):
    self.school_id = school_id
    self.robots_info = ['']
    self.crawl_time = crawl_time

  def scrape_scores(self):
    page_num = 1
    keepGoing = True
    while (keepGoing):
      print("Scraping page: " + page_num)
      keepGoing = self.read_page(page_num)
      page_num += 1
      self.crawl_delay()


  #Scrapes web page, returns bool to scrape scores. if true keep scraping else, no more content
  # Refactor to try except
  def read_page(self, n):
    link = 'https://www.ratemyprofessors.com/filter/professor/?&page={}&queryoption=TEACHER&queryBy=schoolId&sid={}'.format(n,self.school_id)
    page = requests.get(link)
    data = json.loads(page.content)

    #Way to stop looping page number
    if(len(data['professors']) < 1):
      print("Reached last page. exiting scrape loop")
      return False #return false: no more page content to scrape. Scrape scores stops loop
    
    profNum = 0
    while (profNum < len(data['professors'])):
      fName = data['professors'][profNum]['tFname'] + data['professors'][profNum]['tLname'] 
      print(fName)
      profNum += 1
    return True


  def crawl_delay(self):
    time.sleep(self.crawl_time)







###
if __name__ == '__main__':
  rmp = RMP(727)
  rmp.scrape_scores()