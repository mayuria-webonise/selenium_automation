
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import sys
import re
from random import randint

class Automation:

    def date_parser(self):
        with open("file","r") as f:
            dates=f.readlines()
            xpath=".//*[@id='checkIn']"
            for date in dates:
                start_date=date.split("/")
                input_date=int(start_date[0])
                input_month=int(start_date[1])
                input_year=int(start_date[2])
                self.get_date(xpath,input_date,input_month,input_year)
                xpath=".//*[@id='checkOut']"


    def get_date(self,xpath,input_date,input_month,input_year):
        "validate date and automate journey dates"

        if input_month<int(time.strftime("%m")):
            print "input month is less than current month"
            exit()
        elif input_date<int(time.strftime("%d")) and input_month==int(time.strftime("%m")):
            print "date is less than current date"
            exit()
        if input_year!=int(time.strftime("%Y")):
            print "cannot book flights for next year or previous year"
            exit()

        calender_block=self.driver.find_element_by_xpath(xpath)
        calender_block.click()
        calender=self.driver.find_element_by_class_name("calendar")
        months=calender.find_elements_by_class_name("month")

        m=months[0]
        caption= m.find_elements_by_class_name("caption")
        #print caption[0].text
        monthstamp=time.strptime(caption[0].text,"%B %Y")
        month=monthstamp[1]
        #print month
        if input_month < month:

            diff=month-input_month
            for i in range(diff):
                ele = self.driver.find_element_by_class_name("prev")
                ele.click()
                time.sleep(5)
            months = calender.find_elements_by_class_name("month")

        if input_month>month:

            diff=input_month-month

         #   print diff
            for i in range(diff):

                ele = self.driver.find_element_by_class_name("next")
                ele.click()
                time.sleep(3)
            months = calender.find_elements_by_class_name("month")

        for m in months:
            time.sleep(5)
            dates=m.find_elements_by_tag_name("a")
            for date in dates:
                if int(date.text)==input_date:
                    date.click()
                    return


        time.sleep(5)


    def initializeDriver(self):
        "initialize the driver with firefox"
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.tripadvisor.in")
        self.automate()

    def handle_popups(self):
        "handles the pop up appeared"
        handles = self.driver.window_handles
        main_window = self.driver.current_window_handle
        #print "main" + main_window


        while len(handles) >= 2:
            if len(handles) > 1:

                for handle in handles:
                    if handle!=main_window:
                        try:

           #                 print "closed" + handle
                            self.driver.switch_to.window(handle)
                            self.driver.close()
                        except:
                            continue

         #       print "before switched" + main_window
                self.driver.switch_to.window(main_window)
          #      print "switched" + main_window

            else:
                time.sleep(5)
            handles = self.driver.window_handles

    def find_price(self):

        "finds the minimum price from list displayed"
        element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flightList")))

        divisions = self.driver.find_element_by_class_name("flightList")
        divs = divisions.find_elements_by_tag_name("span")
        self.price = sys.maxint
        if (len(divs) == 0):
            print "no div tags found"
        else:
            for div in divs:
            #    print div.get_attribute("class")
                if div.get_attribute("class") == "price":
                    nos = re.findall(r"\d+", div.text)
                    no = nos[0] + nos[1]
             #       print no

                    if int(no) < self.price:
                        self.price = int(no)
                        self.price_div = div
                else:
                    continue
            print "price" + str(self.price)
            self.price_div.click()

    def select_any_from_more(self):

        "clicks on more option and selects the random option"
        more_item=WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH,".//*[@id='taplc_flight_results_sorts_0']/div[1]/span[2]/span[4]/label")))
        more_item.click()
        more=self.driver.find_element_by_id("sort_sub_items")
        divs=more.find_elements_by_tag_name("div")
        random_no=randint(0,4)
        div=divs[random_no]
        div.click()



    def automate(self):

        "main automation function"
        element=self.driver.find_element_by_xpath(".//*[@id='rdoFlights']/div/span")
        element.click()

        source =self.driver.find_element_by_xpath(".//*[@id='metaFlightFrom']")
        source.clear()
        source.send_keys('Pune')
        source_autofill = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "autocompleter-queried")))
        source_autofill.click()


        dest= self.driver.find_element_by_xpath(".//*[@id='metaFlightTo']")
        dest.send_keys('Delhi')

        self.handle_popups()
        dest_autofill=WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "autocompleter-selected")))
        dest_autofill.click()

        self.date_parser()
        adult = self.driver.find_element_by_id("fadults")
        adult.click()
        travellers=adult.find_elements_by_tag_name("option")
        "generate the random no of travellers"
        persons=randint(1,6)
        for traveller in travellers:
            if traveller.get_attribute("value")==str(persons):
                traveller.click()
                break



        search_flights= self.driver.find_element_by_id("SUBMIT_FLIGHTS")
        search_flights.click()


        element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='ui_close_x']")))
        element.click()

        self.handle_popups()
        #select random option from more tag
        self.select_any_from_more()
        "finds min price from list provided"

        time.sleep(20)
        self.find_price()




if __name__ == "__main__":
    a= Automation()
    Automation.initializeDriver(a)