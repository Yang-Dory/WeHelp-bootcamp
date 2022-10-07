import urllib.request as req
import json
src='https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json'
with req.urlopen(src) as response:
    data=json.load(response)
    alldata=data['result']['results']
with open("data.csv", "w", encoding="utf-8")as file:
   for data in alldata:
      date=data["xpostDate"]
      address=data["address"]
      http=data["file"].replace("jpg", "jpg,").replace("JPG", "JPG,")
      http=http.split(",")
      if int(date[:4])>=2015:
         result=data["stitle"], address[5:8], data["longitude"], data["latitude"], http[0]
         string=str(result)
         final=string.replace("'", "").replace("(", "").replace(")", "")
         file.write(final+"\n")


titledata={"[好雷]":[], "[普雷]":[], "[負雷]":[]}
def getdata(url):
   request=req.Request(url, headers={
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
      })
   with req.urlopen(request) as response:
      data=response.read().decode("utf-8")
   import bs4
   root=bs4.BeautifulSoup(data, "html.parser")
   titles=root.find_all("div", class_="title")
   for title in titles:
      if title.a !=None and "[好雷]" in title.a.string:
         titledata["[好雷]"]+=[title.a.string]
      elif title.a !=None and "[普雷]" in title.a.string:
         titledata["[普雷]"]+=[title.a.string]
      elif title.a !=None and "[負雷]" in title.a.string:
         titledata["[負雷]"]+=[title.a.string]
   nextlink=root.find("a", string="‹ 上頁")
   return nextlink["href"]  
url="https://www.ptt.cc/bbs/movie/index.html"
count=0
while count<10:
   url="https://www.ptt.cc"+getdata(url)
   count+=1
with open("movie.txt", "w", encoding="utf-8")as file:
   for title, fulltitle in titledata.items():
      for i in fulltitle:
         file.write(i+"\n")



