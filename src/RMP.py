# Alexander Shelton
# RMP kv seeder
# This program will take in a school-id and a http address
# Program scrapes all professors names and scores and sends the data to be stored in kv to webserver
# Can remove the "send_to_kv()" and add the entries to a dict if you want to save the data locally. otherwise saved as json kv on server



import requests
import json
import time
import sys  
import argparse

# Rate my professor scraper
# Scrapes all professors names & scores
# Sends to server
# robots.txt states crawl time of 10 secconds

class RMP:
  def __init__(self, school_id, crawl_time=10):
    self.school_id = school_id
    self.scores = {}
    self.robots_info = ['']
    self.crawl_time = crawl_time

  def scrape_scores(self) -> dict:
    page_num = 1 #start page num at zero 
    keepGoing = True
    while (keepGoing):
      print("\nScraping page: [" + str(page_num) + "]\n") #ugly print clearing console up a little 
      keepGoing = self.read_page(page_num)
      page_num += 1
      self.crawl_delay()
    
    return self.scores


  #Scrapes web page, returns bool to scrape scores. if true keep scraping else, no more content
  # Refactor to try except
  def read_page(self, n) -> bool:
    link = 'https://www.ratemyprofessors.com/filter/professor/?&page={}&queryoption=TEACHER&queryBy=schoolId&sid={}'.format(n,self.school_id)

    try:
        page = requests.get(link)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
        print('Server taking too long. Try again later')
        exit(1)

    data = json.loads(page.content)

    #Way to stop looping page number
    if(len(data['professors']) < 1):
      print("Reached last page. exiting scrape loop")
      return False #return false: no more page content to scrape. Scrape scores stops loop
    
    profNum = 0
    while (profNum < len(data['professors'])):
      name = data['professors'][profNum]['tFname'] + data['professors'][profNum]['tLname']
      score = data['professors'][profNum]['overall_rating']
      #self.send_to_kv(name, score) #seeds the server

      self.scores[name] = score;
      profNum += 1

    return True



  #used to delay requests in between scraping: RMP states a crawl rate of 10sec 
  def crawl_delay(self) -> None:
    time.sleep(self.crawl_time)




def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='school id is needed to scrape scores')

    args = parser.parse_args()
    score_file = open('scores.json', 'w')

    rmp = RMP(args.id)
    obj = rmp.scrape_scores()

    json.dump(obj, score_file)
    score_file.close()

    return 0

# Code to seed data base: can take out "send_to_kv()" and save to dict if neccesary
if __name__ == '__main__':
    exit(main())
