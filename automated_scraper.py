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
        articlePublishedDate = driver.find_element_by_xpath("//input")
        
        # Switches to HTML Frame
        driver.switch_to.frame("text_ifr")
        content = driver.find_element_by_id("tinymce")
        content.click()
        content.send_keys(Keys.CONTROL, "a")
        content.send_keys(Keys.CONTROL, "c")
        
        driver.back()
        
    driver.execute_script("window.open('https://www.adzu.edu.ph/adzu-ak-login/', 'new window')")
    driver.switch_to.window(driver.window_handles[1])
    
    userField = driver.find_element_by_xpath("//input[@name='log' or id='user_login']")
    userField.send_keys(os.getenv("WP_USERNAME"))

    passwordField = driver.find_element_by_xpath("//input[@name='pwd' or id='user_pass']")
    passwordField.send_keys(os.getenv("WP_PASSWORD"))
    
    loginButton = driver.find_element_by_xpath("//input[@name='wp-submit' or id='wp-submit']")
    loginButton.click()
    
    posts = driver.find_element_by_xpath("//div[contains(text(),'Posts')]")
    action.move_to_element(posts).perform()
    
    addPost = driver.find_element_by_xpath("//a[contains(text(),'Add New')]")
    addPost.click()
    
    # Tells the browser to wait for 10 seconds
    driver.implicitly_wait(10)
    
    # Sets article title
    postTitle = driver.find_element_by_xpath("//textarea[@id='post-title-0']")
    postTitle.send_keys(articleTitle)
    postTitle.send_keys(Keys.TAB)
    
    # Sets article content
    postContent = driver.switch_to.active_element
    postContent.send_keys(Keys.CONTROL, "v")
    
    documentTab = driver.find_element_by_xpath("//button[contains(text(),'Document')]")
    documentTab.click()

    categoryButton = driver.find_element_by_xpath("//button[contains(text(),'Categories')]")
    categoryButton.click()

    categorySearch = driver.find_element_by_xpath("//input[@class='editor-post-taxonomies__hierarchical-terms-filter']")
    categorySearch.send_keys(currentCategory)
    
    selectSidebar = category = Select(driver.find_element_by_name("cs_replacement_custom-sidebar"))
    selectSidebar.select_by_visible_text("Grade School")
        
        
        