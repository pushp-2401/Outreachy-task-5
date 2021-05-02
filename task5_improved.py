import pywikibot
from pywikibot import pagegenerators
from pywikibot.data import api
import numpy as np
import requests
enwiki = pywikibot.Site('en', 'wikipedia')
# and then to wikidata
enwiki_repo = enwiki.data_repository()
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()


targetcats = ['Category:Articles_without_Wikidata_item']
pages =  enwiki.querypage('UnconnectedPages')
#for page in pages:
    # print(page.title())
q1 = [];
l1 = [];


class Solution:
   def solve(self, s0, s1):
      s0 = s0.lower()
      s1 = s1.lower()
      s0List = s0.split(" ")
      s1List = s1.split(" ")
      return len(list(set(s0List)&set(s1List)))
ob = Solution()

searchterm = input('Input search term: ')

def search_entities(site, itemtitle):
     params = { 'action' :'wbsearchentities', 
                'format' : 'json',
                'language' : 'en',
                'type' : 'item',
                'search': itemtitle}
     request = api.Request(site=site, parameters=params)
     return request.submit()
wikidataEntries = search_entities(enwiki_repo, searchterm)
if wikidataEntries['search'] != []:
    results = wikidataEntries['search']
    numresults = len(results)
    for i in range(0,numresults):
        qid = results[i]['id']
        label = results[i]['label']
        title = searchterm
        if title.casefold() == label.casefold() :
            q1.append(qid)
            l1.append(label)
            print (qid + " - " + label)

print(q1)
count = []
d1 = input("Please give some descreption about the item you are searching for?")

for qid in q1:
 item = pywikibot.ItemPage(repo, str(qid))
 item_dict = item.get()
 d2 = item_dict["descriptions"]['en'] 
 common_word = ob.solve(d1,d2) # gives the common words between description given by user and description given by wikidata for different q-values.
 count.append(common_word)
 
 
max_match = max(count)
max_index = count.index(max_match)
print(q1[max_index])