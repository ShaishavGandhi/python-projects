import smtplib,requests
from bs4 import BeautifulSoup
from lxml import html
import time,os
import datetime


def getXmlData():
	xml = requests.get('https://sfbay.craigslist.org/search/apa?format=rss&hasPic=1&max_price=1600&min_price=1000&postal=94118&search_distance=5&sort=date')
	return BeautifulSoup(xml.content,'xml')

 
def sendEmail(to,link):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("shaishgandhi@gmail.com", "albertnewton666")
 
	msg = "Subject: Craigslist Ad\n\nHi,\n\nI saw your ad on CraigsList ("+link+") and I'm interested in the place. \n\nCan you tell me a little bit more about the place? Also, if it's fine with you we can schedule a time when I can come and have a look at the place. \n\nLittle bit about me : I'm a Software Engineer working at Glassdoor. I work Mon-Fri. I'm a quiet person who likes to read, write and play acoustic guitar sometimes. \n\nLet me know.\n\nThanks,\nShaishav"
	server.sendmail("shaishgandhi@gmail.com", to, msg)
	print "Message sent to "+to+" for ad : "+link
	server.quit()

def getEmailFromPostId(post_id):
	try:
		url = "https://sfbay.craigslist.org/reply/sfo/apa/"+str(post_id)
		resp = requests.get(url)
		resp = BeautifulSoup(resp.content)
		email = resp.find_all("ul",{"class" : "pad"})[0]
		return email.text.strip()
	except:
		return ""


def getIdFromLink(link):
	endIndex = link.index(".html")
	endIndex = endIndex
	startIndex = link.index('apa/')
	startIndex = startIndex+4
	post_id = link[startIndex:endIndex]
	return post_id

def writeToFile(visited):
	f = open('craigslist.txt',"a")
	for link in visited:
		f.write(link+"\n")
	f.close()

def doesLinkExist(link):
	f = open('craigslist.txt',"w+")
	repo = f.read()
	for line in repo:
		if line == link:
			f.close()
			return True
	f.close()
	return False


visited = []
while True:
	xml = getXmlData()
	items = xml.find_all('item')
	for item in items:
		link = item.link.text
		if link not in visited:
			visited.append(link)
			post_id = getIdFromLink(link)
			email = getEmailFromPostId(post_id)
			if email!="":
				sendEmail(email,link)
		else:
			print "Already sent email for this posting"
	#writeToFile(visited)
	print "Sleeping now... It's "+str(datetime.datetime.now().time())
	time.sleep(60*60)

 
