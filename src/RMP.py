# Alexander Shelton
# RMP kv seeder
# This program will take in a school-id and a http address
# Program scrapes all professors names and scores and sends the data to be stored in kv to webserver
# Can remove the "send_to_kv()" and add the entries to a dict if you want to save the data locally. otherwise saved as json kv on server






import requests
import json
import time
import sys  



# Rate my professor scraper
# Scrapes all professors names & scores
# Sends to server
# robots.txt states crawl time of 10 secconds

# https://www.ratemyprofessors.com/filter/professor/?&page=1&queryoption=TEACHER&queryBy=schoolId&sid=<schoolid>

class RMP:
  def __init__(self, school_id, url, crawl_time=10):
    self.school_id = school_id
    self.robots_info = ['']
    self.url = url
    self.crawl_time = crawl_time

  def scrape_scores(self):
    page_num = 1 #start page num at zero 
    keepGoing = True
    while (keepGoing):
      print("\nScraping page: [" + str(page_num) + "]\n") #ugly print clearing console up a little 
      keepGoing = self.read_page(page_num)
      page_num += 1
      self.crawl_delay()
    
    print("Outside of the scrape loop")


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
      name = data['professors'][profNum]['tFname'] + data['professors'][profNum]['tLname']
      score = data['professors'][profNum]['overall_rating']
      print(name + ' : ' + score)
      self.send_to_kv(name, score) #seeds the server
      profNum += 1
    return True


  def crawl_delay(self):
    time.sleep(self.crawl_time)



  #sends a put request to the db api url
  #If the scraped value is 'N/A' we are not sending the score
  def send_to_kv(self, name, score):
    if(score == 'N/A'): return
    
    #change this line to work with your api
    put_url = self.url + '/'+ name + '/' + score #building post url from inputted url
    r = requests.put(put_url)
    if r.status_code != 200:
      print("There was an error sending {}'s score to the kv".format(name))



def printDefaults():
  print("Usage: \n 1st argument is school_id\n seccond argument is url for posting the data to")
  print("Example: python RMP.py 690 http://myDomain.com/api")




# Code to seed data base: can take out "send_to_kv()" and save to dict if neccesary
if __name__ == '__main__':
  if(len(sys.argv) < 2):
    print("Missing arguments")
    printDefaults()
    exit(1)
  
  print(sys.argv)
  rmp = RMP(sys.argv[1], sys.argv[2])
  rmp.scrape_scores()
  exit(0)