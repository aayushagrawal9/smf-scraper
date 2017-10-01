from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='smf-scraper',
      version="0.1",
      description='SMF Scraper to download RAW HTML of all pages of threads',
      long_description=readme(),
      author='Aayush Agrawal',
      author_email='aayushagrawal2096@gmail.com',
      license='MIT',
      url='https://github.com/aayushagra/smf-scraper',
      packages=['pysmfscrape'],
      entry_points={'console_scripts': ['pysmfscrape=pysmfscrape.cli:scrape']},
      test_suite='test_pysmfscrape',
      keywords=['smf', 'scraper'],
      zip_safe=False,
      install_requires=[
          'mechanize',
          'bs4',
          'click']
      )