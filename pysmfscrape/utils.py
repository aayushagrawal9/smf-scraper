def is_login_page(soup):
	if soup.title.text == "Login":
		print "Login Page"
		return True
	else:
		return False

def pages_in_thread(soup):
	pagelinks = soup.find_all(class_="pagelinks")
	if len(pagelinks) > 0:
		a = pagelinks[0].find_all("a")
		try:
			pagenum = a[-2].text
		except:
			pagenum = 1

		try:
			return int(pagenum)
		except:
			print "Error: Could not determine pages in thread"
			return 1
	else:
		return 1