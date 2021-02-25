#!/data/data/com.termux/files/usr/bin/python
# ZippyShare url finder with (gugel search)
# dtz-aditia © 2020.02.25

from requests import Session, logging
from random import choice
from bs4 import BeautifulSoup, re, sys, os

logging.basicConfig(format="%(message)s",level=logging.INFO)
# <-- harus windows/safari biar style nya dekstop -->
UA_LIST = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
"Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
]

class ZipFinder(object):
	def __init__(self, dork):
		self.session = Session()
		self.session.headers["User-Agent"] = choice(UA_LIST)
		self.VALID_URL = re.compile(r"https://www\d+.zippyshare.com/v/[^/]+/file.html")
		self.dork = dork
		self.count = 1
#		self.countFR = 0
		self.url = []
		self.domain = "https://www.google.com"
		self.__main__(self.dork)

	def _parse(self, raw):
		raw = raw.text if hasattr(raw,"text") else raw
		return BeautifulSoup(raw,"html.parser")

	def _gets(self, page):
		for v in list(set(self.VALID_URL.findall(page))):
			if v not in self.url:
				logging.info(
					f"[*] !- ADD -> {v} -> {self.count}")
				self.url.append(
					v)
				self.count +=1

	def _writes(self, data):
		logging.info(
			f"[*] !- SAVING RESULT -> {len(data)} URL")
		data = "\n".join(data) if isinstance(data,list) else data
		with open("url.txt","w") as f:
			f.write(data)
		logging.info(
			"[*] !- SAVED TO -> ``url.txt``")

	def _format(self, raw):
		raw = self._parse(raw) if isinstance(raw, str) else raw
		return [_["href"] for _ in raw.findAll("a",class_="fl") if _["href"].startswith("/search")]

	def __main__(self, dork):
		page = 0
		try:
			logging.info(
				f"[*] !- GETTING URL WITH DORK -> {dork}"
				"\n[*] \x1b[91m!- PRESS CTRL + C FOR STOP!\x1b[0m")
			_page = self.session.get(
				f"{self.domain}/search",params={"q":dork}).text
			self._gets(_page)
			logging.info(
				f"[*] !- SUCCESS ADD -> {len(self.url)} URL"
				f"\n[*] !- GETTING NEXT PAGE!")
			nch = self._format(_page)
			if len(nch) != 0:
				while len(nch):
					index = nch[page]
					_pg = self.session.get(self.domain + index).text
					self._gets(_pg)
					page +=1
					if index == nch[-1]:
						nch = self._format(_pg)[5:]
						page = 0
			else:
				logging.info(
					"[*] !- NOTHING MORE RESULT!")
			logging.info(
				f"[*] !- SUCCESS GETTING -> {len(self.url)} URL")
			self._writes(self.url)
		except KeyboardInterrupt:
			logging.info(
				"[*] \x1b[91m!- STOPED BY USER!\x1b[0m")
			self._writes(self.url)
		

if __name__=="__main__":
	if len(sys.argv) < 2:
		exit(
			"usage : finder.py <dork>\n"
			"example : python main.py intext:'jav' site:'zippyshare.com'")
	else:
		os.system("xdg-open https://youtube.com/channel/UCfTsQXMv33z6geEbaeZMi5w")
		ZipFinder(" ".join(sys.argv[1:]))

#contact : https://t.me/aditia_dtz
