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

output_path = '/Users/...' # Your output file path. Use ABSOLUTE PATH!
start_point = 'https://www.slideshare.net/ZachBenedict3/zachary-benedict-resume-71651324'  # The page start to scrape
username = 'example@gmail.com' # Your Linkedin account
password = 'password' # Your Linkedin password
search_depth = 2 # Depth you want search into

main_window_handle = None
url_set = set()
basic_url = "https://www.slideshare.net"
num_of_file = 0

def init_driver():

    chromeOptions = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': output_path, "profile.managed_default_content_settings.images": 2}
    chromeOptions.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chromeOptions)
    driver.wait = WebDriverWait(driver, 5)
    return driver

def login(driver):
    print "Logging into slideshare ...\n"
    driver.get(start_point)
    login_btn = driver.find_element_by_id('login')
    login_btn.click()
    time.sleep(3)
    

    login_with_linkedin_btn = driver.find_element_by_class_name('j-linkedin-connect')
    login_with_linkedin_btn.click()

    print "Switching to the popup ...\n"
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
    print "Login Successfully!\n"

def crawler(driver,count,start_url):
    global num_of_file
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
        if num_of_file != 0 and num_of_file % 5 == 0:
            print str(num_of_file) + " files have been download!\n"
        print "Downloading " + driver.current_url + " ...\n"
        download_button.click()
        url_set.add(driver.current_url)
        num_of_file = num_of_file + 1

    time.sleep(3)

    for url in related_url_list:
        crawler(driver,count+1,basic_url+url)


if __name__ == "__main__":
    driver = init_driver()
    while not main_window_handle:
        main_window_handle = driver.current_window_handle

    login(driver)
    print "Starting download files ...\n"
    crawler(driver,0,start_point)
    driver.quit()
