####################################
#
#  Terminal Craigslist 
#
#
#  By David Valenza
#
#  Usage: python clperm.py
#    or   python clterm.py searchterm
#
#  TTD
#  -Dont show non-local results
#  -if no args given show all
#  -ask to narrow searches with regex

import readline
import cllist, cllib
import sys
from bs4 import BeautifulSoup
import urllib2
import re


#global for counting
total = 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MyCompleter(object):  # Custom completer
    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options 
                                    if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try: 
            return self.matches[state]
        except IndexError:
            return None

def scanCL(link):
  subtotal = 0 
  page = urllib2.urlopen(link).read()
  soup = BeautifulSoup(page)
  data = soup.findAll("a")
  location = soup.findAll('span', attrs={ 'class':'pnr'})
  for x in range (19,118): #main links start at 19th 'a' into html
   # matchObj = re.search( r'(.*)'+ sys.argv[1] +'(.*?).*', str(data[x]) ,re.M|re.I)
    #if matchObj:
         try: 
           locationx = location[(x-19)/4].findAll("small")[0].string #Must divide index by 4 since main link is every 4 'a's
         except IndexError:
           locationx = ""
         print  bcolors.WARNING+"[+] " + str(locationx) +bcolors.ENDC+" "+ bcolors.OKBLUE + data[x].contents.pop()  + bcolors.ENDC +" | "+"http://boston.craigslist.org" + data[x]['href']
         subtotal+=1
         global total
         total +=1
  if subtotal >= 1:       
    print bcolors.OKGREEN + "[*] " + str(subtotal) + " Results found" + bcolors.ENDC   
  else:
    print bcolors.FAIL + "[-] No Results.." + bcolors.ENDC 

categories = ["location","sub_location","category","community",
         "events","for_sale","gigs","housing","jobs",
         "personals","services"]

#My attempt to consolidate code...
#for x in categories:
#  completer = MyCompleter(list(cllist.?????))
#  readline.set_completer(completer.complete)
#  readline.parse_and_bind('tab: complete')
#  location = raw_input("Location: ")  

completer = MyCompleter(list(cllist.location))
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')
location = raw_input("Location: ")

#Sub Location must be different based on Primary Location!!
#must fix!
#gives boston every time
if location == "boston":
    completer = MyCompleter(list(cllist.sub_location))
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')
    sub_location = raw_input("Area: ")


completer = MyCompleter(list(cllist.category))
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')
category = raw_input("category: ")

if category == "community":
  completer = MyCompleter(list(cllist.community))
  readline.set_completer(completer.complete)
  readline.parse_and_bind('tab: complete')
  community = raw_input("community: ")
  for sub in cllib.communityx:
      if sub[0] == community:#must change to give scan only sub1 as param
          if len(sys.argv)>1:
              url="http://boston.craigslist.org/search/"+sub[1]+"?query="+sys.argv[1]
          else:
              url="http://boston.craigslist.org/search/"+sub[1]
          scanCL(url)
elif category == "events":
  completer = MyCompleter(list(cllist.events))
  readline.set_completer(completer.complete)
  readline.parse_and_bind('tab: complete')
  events = raw_input("events: ")
elif category == "for sale":
  completer = MyCompleter(list(cllist.for_sale))
  readline.set_completer(completer.complete)
  readline.parse_and_bind('tab: complete')
  for_sale = raw_input("for_sale: ")
elif category == "gigs":
  completer = MyCompleter(list(cllist.gigs))
  readline.set_completer(completer.complete)
  readline.parse_and_bind('tab: complete')
  gigs = raw_input("gigs: ")
elif category == "housing":
  completer = MyCompleter(list(cllist.housing))
  readline.set_completer(completer.complete)
  readline.parse_and_bind('tab: complete')
  housing = raw_input("housing: ")
elif category == "jobs":
  completer = MyCompleter(list(cllist.jobs))
  readline.set_completer(completer.complete)
  readline.parse_and_bind('tab: complete')
  jobs = raw_input("jobs: ")
  for sub in cllib.jobsx:
      if sub[0] == jobs:#must change to give scan only sub1 as param
          url="http://boston.craigslist.org/search/"+sub[1]+"?query="+sys.argv[1]
          scanCL(url)
elif category == "personals":
  completer = MyCompleter(list(cllist.personals))
  readline.set_completer(completer.complete)
  readline.parse_and_bind('tab: complete')
  personals = raw_input("personals: ")
elif category == "services":
  completer = MyCompleter(list(cllist.services))
  readline.set_completer(completer.complete)
  readline.parse_and_bind('tab: complete')
  services = raw_input("services: ")
