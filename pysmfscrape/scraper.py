import mechanize
from bs4 import BeautifulSoup
import traceback
import time

from utils import is_login_page, pages_in_thread

pagecount = 0

def login(br, username, password):
	br.select_form("frmLogin")
	br["user"] = username
	br["passwrd"] = password
	for i in range(0, len(br.find_control(type="checkbox").items)):
		br.find_control(type="checkbox").items[i].selected =True
	response = br.submit()
	with open("login.html", "wb") as file:
		file.write(response.read())

def fetch_page(br, baseurl, threadno, pageno, delay):
	time.sleep(delay)
	url = baseurl + str(threadno) + "." + str(pageno*15)

	global pagecount
	pagecount += 1
	print "[%d - %d] URL: %s" % (threadno, pagecount, url)

	return br.open(url, timeout=10).read()

def fetch_error(threadno, pageno, baseurl, exception, enable_traceback):
	url = baseurl + str(threadno) + "." + str(pageno*15)
	print "Error fetching URL: %s" % (url)

	if enable_traceback is True:
		print exception
	else:
		print "Use flag --traceback to print full traceback"

def downloadThread(threadno, baseurl, br, username, password, path, delay, enable_traceback, pageno = 0):
	try:
		page = fetch_page(br=br, baseurl=baseurl, threadno=threadno, pageno=pageno, delay=delay)
	except KeyboardInterrupt:
		raise(KeyboardInterrupt)
	except:
		return fetch_error(threadno, pageno, baseurl, traceback.format_exc(), enable_traceback)

	soup = BeautifulSoup(page, "html.parser")

	if is_login_page(soup):
		if username is not None:
			login(br, username, password)
			downloadThread(threadno=threadno, baseurl=baseurl, br=br, username=username, password=password, path=path, delay=delay, enable_traceback=enable_traceback, pageno=pageno)
	else:
		with open("%s/%s-%s.html" % (path, str(threadno), str(pageno)), "wb") as file:
			file.write(page)

		if pageno == 0:
			pages = pages_in_thread(soup)

			for j in range(1, pages):
				downloadThread(threadno=threadno, baseurl=baseurl, br=br, username=username, password=password, path=path, delay=delay, enable_traceback=enable_traceback, pageno=j)

	br.clear_history()

def scrape(baseurl, start, end, delay, path, username, password, enable_traceback):
	br = mechanize.Browser()
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1) # Follows refresh 0 but not hangs on refresh > 0

	import time
	start_time = time.time()

	for i in range(start, end+1):
		downloadThread(threadno=i, baseurl=baseurl, br=br, username=username, password=password, path=path, delay=delay, enable_traceback=enable_traceback)

	time_taken = time.time() - start_time

	num_threads = end-start
	print "Processed %s threads in %s seconds, average time: %s" % (num_threads, time_taken, time_taken/num_threads)