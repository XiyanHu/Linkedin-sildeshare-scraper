from selenium import webdriver
import time
import pickle
import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

output_path = '/Users/appleapple/Desktop/for\ fun/shareslide/files'
start_point = 'https://www.slideshare.net/WanWei3/resumewei-wanfulltime2?qid=f8af5f02-a362-4075-ae5b-03be5d52fe99&v=&b=&from_search=25'
username = 'yanjiu414@163.com'
password = 'qazxcdewq123'
main_window_handle = None
url_set = set()
search_depth = 2
basic_url = "https://www.slideshare.net"

def init_driver():
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': output_path }
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
    driver.wait = WebDriverWait(driver, 5)
    return driver

def login(driver):
    driver.get(start_point)
    login_btn = driver.find_element_by_id('login')
    login_btn.click()
    time.sleep(3)
    

    login_with_linkedin_btn = driver.find_element_by_class_name('j-linkedin-connect')
    login_with_linkedin_btn.click()

    signin_window_handle = None
    while not signin_window_handle:
        for handle in driver.window_handles:
            if handle != main_window_handle:
                signin_window_handle = handle
                break
    driver.switch_to.window(signin_window_handle)
    
    time.sleep(3)

    try:
        username_field = driver.wait.until(EC.presence_of_element_located((By.ID,"session_key-oauth2SAuthorizeForm")))
        password_field = driver.find_element_by_id('session_password-oauth2SAuthorizeForm')
        login_button = driver.find_element_by_class_name('allow')
        username_field.send_keys(username)
        time.sleep(1)
        password_field.send_keys(password)
        time.sleep(1)
        login_button.click()
        time.sleep(5)
    except TimeoutException:
        print("TimeoutException! Username/password field or login button not found.")
    print "haha"

def crawler(driver,count,start_url):
    if count == search_depth:
        return
    if count == 0:
        driver.switch_to.window(main_window_handle)
        pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
        driver.get(start_point)
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

    driver.get(start_url)

    HTML = driver.page_source
    soup = BeautifulSoup(HTML,"html.parser")
    related_list = soup.find_all("a",{"j-recommendation-tracking"})
    related_url_list = []
    for item in related_list:
        related_url_list.append(item.get("href"))

    #download current page file
    download_button = driver.find_element_by_id("slideshow-actions").find_element_by_class_name("download")
    if download_button and driver.current_url not in url_set:
        download_button.click()
        url_set.add(driver.current_url)
    time.sleep(3)

    for url in related_url_list:
        crawler(driver,count+1,basic_url+url)


    
def test(driver):
    driver.get(start_point)
    HTML = driver.page_source
    soup = BeautifulSoup(HTML,"html.parser")
    related_list = soup.find_all("a",{"j-recommendation-tracking"})
    related_url_list = []
    for item in related_list:
        related_url_list.append(item.get("href"))
    print related_url_list
    driver.get(basic_url+related_url_list[0])
    


if __name__ == "__main__":
    driver = init_driver()
    while not main_window_handle:
        main_window_handle = driver.current_window_handle

    login(driver)
    crawler(driver,0,start_point)
    # test(driver)
    driver.quit()
