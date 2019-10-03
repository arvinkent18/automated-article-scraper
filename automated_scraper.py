from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from dotenv import load_dotenv
import pyperclip
import os

if __name__ == "__main__":
    load_dotenv(verbose=True)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.get(os.getenv("DOMAIN"))
    wait = WebDriverWait(driver, 10)
    action = ActionChains(driver)

    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    
    userField = wait.until(ec.visibility_of_element_located((By.XPATH, "//input[@name='username' or id='modlgn_username']")))
    userField.send_keys(username)

    passwordField = driver.find_element_by_xpath("//input[@name='passwd' or id='modlgn_passwd']")
    passwordField.send_keys(password)

    loginButton = driver.find_element_by_link_text('Login')
    loginButton.click()

    articleManagerButton = driver.find_element_by_link_text("Article Manager")
    articleManagerButton.click()

    category = Select(driver.find_element_by_name("filter_sectionid"))
    category.select_by_visible_text("Grade School")
    
    pageLimit = Select(driver.find_element_by_name("limit"))
    pageLimit.select_by_visible_text("all")
    
    articleList = []
        
    numberOfArticles = len(driver.find_elements_by_xpath("//table[@class='adminlist']//tbody//tr//td[3]//a"))
    
    print("Number of articles:{}".format(numberOfArticles))
    
    for index in range(numberOfArticles):
        # Gets Article
        article = driver.find_element_by_xpath("//table[@class='adminlist']//tbody//tr[{}]//td[3]//a".format(index+1))
        article.click()
        
        # Gets Article Title
        articleTitle = driver.find_element_by_xpath("//input[@name='title']").get_attribute("value")
        print(articleTitle)
        
        # Gets Article Category
        articleCategory = Select(driver.find_element_by_id("catid"))
        currentCategory = articleCategory.first_selected_option.text
        print(currentCategory)
        
        # Gets Published Date
        articlePublishedDate = driver.find_element_by_xpath("//input[@name='details[created]']").get_attribute("value")
        print(articlePublishedDate)
        
        # Switches to HTML Frame
        driver.switch_to.frame("text_ifr")
        content = driver.find_element_by_id("tinymce")
        content.click()
        content.send_keys(Keys.CONTROL, "a")
        content.send_keys(Keys.CONTROL, "c")
        copiedContent = pyperclip.paste()
        print(copiedContent)
        
        driver.back()
        
        
        
        
   
        
        