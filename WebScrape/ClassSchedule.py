import os, sys
from lxml import html
import requests
from bs4 import BeautifulSoup
import csv
import selenium
from selenium import webdriver
with open("AllClasses.csv", "w") as csv:
    csv.write('Title, Career, Grading, Class Number, Type, Credits, GE, Status, Available Seats, Enrollment Cap, Enrolled, WaitCap, WaitList\n')
    driver = webdriver.Chrome(r"C:\program files\anaconda3\Scripts\chromedriver.exe")
    url = "https://pisa.ucsc.edu/class_search/index.php"
    driver.get(url)
    driver.find_element_by_xpath("//select[ @ id = 'reg_status']/option[text()='All Classes']").click()
    driver.find_elements_by_xpath("//*[@id='searchForm']/div/div[2]/div[15]/div/input")[0].click()
    number = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/b[3]")
    totalpages = int(int(number.text) / 25) + 1
    count = 0
    for x in range(0, totalpages):
        print("we are at page " + str(x))
        soup = BeautifulSoup(driver.page_source.encode('utf-8'), "lxml")
        classes = soup.findAll("div", {"class": "panel panel-default row"})
        for clas in classes:
            list_of_rows = []
            b = clas.find('a', href=True)
            c = str(b['href'])
            urlspec = "https://pisa.ucsc.edu/class_search/" + c
            page = requests.get(urlspec)
            html = page.content
            soup3 = BeautifulSoup(html, "lxml")
            classTitle = soup3.find("h2")
            career, Grading, classNumber, type, credits, ge, status, numSeats, enrollCap, numEnrolled, waitCap, waitList = soup3.findAll("dd")
            list_of_rows.append([classTitle.text, career.text, Grading.text, classNumber.text, type.text, credits.text, ge.text, status.text, numSeats.text, enrollCap.text, numEnrolled.text, waitCap.text, waitList.text])
            if len(list_of_rows) > 13:
                extraName = len(list_of_rows) - 13
                for t in range(1, extraName):
                    list_of_rows[0] = list_of_rows[0] + list_of_rows[t]
                    list_of_rows.remove(list_of_rows[t])


            csv.write(','.join(str(v) for v in list_of_rows) + "\n")
        try:
            if count > 0:
                driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/a[2]").click()
            else:
                driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[28]/a").click()
            count = count + 1
        except selenium.common.exceptions.NoSuchElementException:
            pass



    # link = "https://steamcommunity.com/market/search?q="
    # page = requests.get(link)
    # html = page.content
    # soup = BeautifulSoup(html, "lxml")
    # numPages = soup.findAll("span", {"class": "market_paging_pagelink"})
    # totalPages = len(numPages) + 1
    # for x in range(1, totalPages):
    #     link = "https://steamcommunity.com/market/search?q=#p" + str(x) + "_popular_desc"
    #     page = requests.get(link)
    #     html = page.content
    #     soup = BeautifulSoup(html, "lxml")
    #     itemlist = soup.find("div", {"id": 'searchResultsRows'})
    #     items = itemlist.findAll("a", {"class": "market_listing_row_link"})
    #     for info in items:
    #         list_of_rows = []
    #         itemName = info.find("span", {"class": "market_listing_item_name"})
    #         itemPrice = info.find("span", {"class": "sale_price"})
    #         numItem = info.find("span", {"class": "market_listing_num_listings_qty"})
    #         list_of_rows.append(itemName)
    #         list_of_rows.append(itemPrice)
    #         list_of_rows.append(numItem)
    #         try:
    #             csv.write(','.join(str(v) for v in list_of_rows) + "\n")
    #         except UnicodeEncodeError:
    #             pass

