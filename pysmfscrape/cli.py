import os
import click

import scraper

@click.command()
@click.option('-d', '--delay', default=0.0, type=float, help='Delay between requests in seconds')
@click.option('-p', '--path', default=None, type=str, help='Folder to save raw HTML response to', required=True)
@click.option('--traceback', is_flag=True, default=False)
@click.option('--prefix', default=None, type=str, help='URL Prefix (See readme)', required=True)
@click.option('--username', default=None, type=str, help='Username for scraping login only pages (Leave blank if none)')
@click.option('--password', default=None, type=str, help='Password for scraping login only pages (Leave blank if none)')
@click.argument('start', type=int)
@click.argument('end', type=int)
def scrape(delay, path, traceback, prefix, username, password, start, end):
	if not os.path.isdir(path):
		print "Error: Path specified is not a valid directory"
		return
	elif not os.access(path, os.W_OK):
		print "Error: Cannot write to specified directory"
		return

	if username is not None or password is not None:
		if username is None or password is None:
			print "Error: Please provide both username and password or leave both blank"
			return

	scraper.scrape(prefix, start, end, delay, path, username, password, traceback)
	

scrape()