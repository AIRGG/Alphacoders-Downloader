from bs4 import BeautifulSoup
import requests as rq
import re, time, threading, sys, datetime

print("Preparing..")
url = "https://wall.alphacoders.com/"

# < === Input Keyword Here === > #
keyword = "naruto"  
pagewant = 2
# < ========================== > #

hit = rq.get(f"{url}search.php?search={keyword}").content

html = BeautifulSoup(hit, "html.parser")

htmlLink = BeautifulSoup(hit, 'xml')
bigtitle = html.find("h1", class_="center title")
if bigtitle is None:
	print(f"Sorry '{keyword}' Not Found.!")
	sys.exit(0)

urlpaging = htmlLink.find('link', {'rel': 'canonical'})['href'].strip()
quickload = bigtitle.text.strip().split(' ')[0]
endpaging = html.find('div', {'id': 'next_button'}).text.strip().split('/')[1]

content = html.find_all(class_="thumb-container-big")

print("Getting Data...")
print("-"*50)
print("FOUND: ", endpaging, " PAGE")
print(f"PARSING: {pagewant} PAGE")
print("-"*50)
linkdownload = "https://api.alphacoders.com/content/get-download-link"
imgall = []

thread = []
thread1 = []

def getLink(idcontent, imgtype, imgserver):
	data = {
		"content_id": idcontent,
		"content_type": "wallpaper",
		"file_type": imgtype,
		"image_server": imgserver
	}
	hit = rq.post(linkdownload, data=data)
	linknya = hit.json()["link"]
	imgall.append(linknya)

def prosesOne(uri):
	hit = rq.get(uri).content
	html = BeautifulSoup(hit, "html.parser")
	content = html.find_all(class_="thumb-container-big")
	for x in content:
		idcontent = x["id"].split("_")[-1]
		# img = x.find("img")["data-src"]
		imgid = x.find("span", class_="download-button")["data-id"]
		imgtype = x.find("span", class_="download-button")["data-type"]
		imgserver = x.find("span", class_="download-button")["data-server"]
		t = threading.Thread(target=getLink, args=(imgid, imgtype, imgserver))
		thread.append(t)

for z in range(1, pagewant+1):
	# uri = f"{urlpaging}{z}"
	uri = f"{urlpaging}/&quickload={quickload}&page={z}"
	print("[PAGE] ->", z, uri)
	t = threading.Thread(target=prosesOne, args=(uri,))
	thread1.append(t)
print("="*30)
print("[WAITT] Getting All..")
print("="*30)
for y in thread1:
	y.start()
for y in thread1:
	y.join()

for x in thread:
	x.start()
# 	print(y)
for i, x in enumerate(thread):
	x.join()
	print("[DONE] =>",imgall[i])

nmfile = f"WP-{keyword}-{datetime.datetime.now().strftime('%Y%m%d %H%M%S')}.txt"
with open(nmfile, 'w') as f:
	for x in imgall:
		f.write("{}\n".format(x))

a = imgall
print("*"*30)
print("KEYWORD: {}".format(keyword))
print("PAGE: {}".format(len(thread1)))
print("ALL PAGE: {}".format(endpaging))
print("CONTENT PER PAGE: {}".format(len(content)))
print("ALL GETTING LINK: {}".format(len(a)-1))
print("ALL LINK: {}".format(int(endpaging)*len(content)))
print(len(content), len(imgall), int(endpaging)*len(content))
print("*"*30)