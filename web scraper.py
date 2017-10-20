# web scraper utility
# Ted Beck -- March 2016
# pulls down tax lien notices from local newspaper aggregator for Georgia
# dumps scraped data as JSON objects into a file; includes lien identifier, description of property, and county of record

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re, json, time

def work():
    # set up web driver and load landing page
    driver = webdriver.Chrome(executable_path = 'c://Windows//chromedriver.exe')
    driver.get('http://www.georgiapublicnotice.com/Search.aspx#content-sub')
    
    # grab elements and populate search fields
    search_elem = driver.find_element_by_name('ctl00$ContentPlaceHolder1$as1$txtSearch')
    search_elem.send_keys('years due')
    exclude_elem = driver.find_element_by_name('ctl00$ContentPlaceHolder1$as1$txtExclude')
    exclude_elem.send_keys('bibb fulton richmond')
    daterange = driver.find_element_by_id('ctl00_ContentPlaceHolder1_as1_divDateRange')
    daterange.click()
    datefrom_elem = driver.find_element_by_name('ctl00$ContentPlaceHolder1$as1$txtDateFrom')
    dateto_elem = driver.find_element_by_name('ctl00$ContentPlaceHolder1$as1$txtDateTo')
    datefrom_elem.clear()
    dateto_elem.clear()
    
    # manually adjust date range
    datefrom_elem.send_keys('3/1/2016')
    dateto_elem.send_keys('3/28/2016')
    
    # start search
    driver.find_element_by_name('ctl00$ContentPlaceHolder1$as1$btnGo1').click()
    
    # give server time to respond and then identify the number of pages to loop
    pagenum = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_lblTotalPages')))
    temp = pagenum.text
    loop_no = re.findall('\d+', temp)
    
    # list = driver.find_elements_by_xpath("//input[starts-with(@name,'ctl00$ContentPlaceHolder1$WSExtendedGridNP1$GridView1$')][@type='submit']")
    
    all_results = []
    # loops through pages in succession and scrapes entries
    for i in range(int(loop_no[0])):
        # give server time to respond to page load
        garbage_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'viewButton')))
        time.sleep(2)
        list = []
        list = driver.find_elements_by_class_name('viewButton')
        # pull down raw text of HTML links through element identifier
        links_list = []
        for item in list:
            links_list.append(item.get_attribute('onclick'))
        # clean HTML links through regular expression
        clean_links = []
        for item in links_list:
            temp = re.findall('(href=\')(.+)(\')', item)
            clean_links.append(temp[0][1])
        # cycle through all links and scrape text
        for j in range(len(clean_links)):
            print('Scraping: ' + clean_links[j])
            driver.get('http://www.georgiapublicnotice.com/' + clean_links[j])
            publication_date = driver.find_element_by_id('ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_lblPublicationDAte').text
            publication_name = driver.find_element_by_id('ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_PublicNoticeDetails1_lblPubName').text
            content = driver.find_element_by_id('ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_lblContentText').text
            all_results.append((publication_name, publication_date, content))
            driver.back()
        # check to see if this is the last page
        if i + 1 == int(loop_no[0]):
            break
        else:
            driver.find_element_by_name('ctl00$ContentPlaceHolder1$WSExtendedGridNP1$GridView1$ctl01$btnNext').click()
    
    # dump scraped data as a JSON object into a file
    f = open('c://Users//James.Beck//Desktop//output14.txt', 'w')
    json.dump(all_results, f)
    f.close()
    driver.close()

def main():
    work()

if __name__ == '__main__':
        main()