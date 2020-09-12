# rate-my-prof-scraper
Web scraped designed to scrape all professors rmp score by school ID


Names are grouped by first and last name.   
example: JohnSmith


## Takes 2 command line arguments
* school-id : which is easy to look up, just look up your professor and the url will have it. 
* server path : this is where you will be sending the professors and scores, probably as key value pairs.  

example usage:
> ./RMP.py 700 http://localhost:8000/api 

## Modifications for not using db
simply remove the 'send-to-kv()' function and pass the prof and score into a dictionary.  
