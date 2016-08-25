
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

    def get_date(self):

        fi=open("file",'r')
        date=fi.readline()
        print date
        startdate=self.driver.find_element_by_xpath(".// *[ @ id = 'date_picker_in_0']")
        day=self.driver.find_element_by_class_name("day day_30")
        startdate.send_keys(date)


    def initializeDriver(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.tripadvisor.in")
        self.automate()

    """def handle_popups(self):
        handles=self.driver.window_handles
        main_window=self.driver.current_window_handle
        print "main" + main_window

        while len(handles)>=2:
            if len(handles)>1:

                for i in range(1,len(handles)):

                    print "closed"+handles[i]
                    self.driver.switch_to.window(handles[i])
                    self.driver.close()

                    self.driver.switch_to.window(main_window)
                    print "switched" + main_window

            else:
                time.sleep(5)
            handles = self.driver.window_handles"""

    def handle_popups(self):
        handles = self.driver.window_handles
        main_window = self.driver.current_window_handle
        print "main" + main_window


        while len(handles) >= 2:
            if len(handles) > 1:

                for handle in handles:
                    if handle!=main_window:
                        try:

                            print "closed" + handle
                            self.driver.switch_to.window(handle)
                            self.driver.close()
                        except:
                            continue

                print "before switched" + main_window
                self.driver.switch_to.window(main_window)
                print "switched" + main_window

            else:
                time.sleep(5)
            handles = self.driver.window_handles

    def find_price(self):
        element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flightList")))

        divisions = self.driver.find_element_by_class_name("flightList")
        divs = divisions.find_elements_by_tag_name("span")
        self.price = sys.maxint
        if (len(divs) == 0):
            print "no div tags found"
        else:
            for div in divs:
                print div.get_attribute("class")
                if div.get_attribute("class") == "price":
                    nos = re.findall(r"\d+", div.text)
                    no = nos[0] + nos[1]
                    print no

                    if int(no) < self.price:
                        self.price = int(no)
                        self.price_div = div
                else:
                    continue
            print "price" + str(self.price)
            self.price_div.click()

    def select_any_from_more(self):
        more_item=WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH,".//*[@id='taplc_flight_results_sorts_0']/div[1]/span[2]/span[4]/label")))
        more_item.click()
        more=self.driver.find_element_by_id("sort_sub_items")
        divs=more.find_elements_by_tag_name("div")
        div=divs[1]
        div.click()



    def automate(self):

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

        #self.get_date()
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



        #print self.driver.current_window_handle
        #time.sleep(20)

        """element = WebDriverWait(self.driver, 20).until(
            self.driver.find_element_by_xpath("//div[@class='ui_close_x']")
        )
        element.click()"""

        """print self.driver.current_window_handle

        print len(self.driver.window_handles)
        li=self.driver.window_handles
        print li
        print li[0]
        print li[1]
        self.driver.switch_to.window(li[1])"""

        #self.handle_popups()
        element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='ui_close_x']")))
        element.click()
        #time.sleep(20)

        """close_popup=self.driver.find_element_by_xpath("//div[@class='ui_close_x']")
        close_popup.click()"""

        self.handle_popups()
        "finds min price from list provided"
        self.select_any_from_more()
        time.sleep(20)
        self.find_price()
        #method code



if __name__ == "__main__":
    a= Automation()
    Automation.initializeDriver(a)