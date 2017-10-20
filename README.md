# web-scraper
Python utility to scrape tax lien notice data from local newspaper aggregator

Uses Selenium web driver to load site.  Main body populates search field terms and sends to server.  Driver uses several elements and presence of tests to know when to fire.  First versions tended to send or attempt to collect data before pages fully loaded.
