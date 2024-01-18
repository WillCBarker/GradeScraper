from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time


site = "https://mymasonportal.gmu.edu/ultra/grades"
path = ''#chromedriver path here
driver = webdriver.Chrome(path)
driver.get(site)
driver.maximize_window()

#--------------------------------

def click_element(element):
    """
    Parameters:
    element (Selenium web element): web element returned from find_element methods
    """
    element.click()

def find_element_ID(id):
    """
    Parameters:
    id (String): id copied from the gmu website's html

    Returns:
    Selenium web element
    """
    return click_element(driver.find_element(By.ID, id))

def find_element_Selector(selector):
    """
    Parameters:
    selector (String): selector copied from the gmu website's css

    Returns:
    Selenium web element
    """
    return driver.find_element(By.CSS_SELECTOR, selector)

def input_text(element, text):
    element.send_keys(text)

def pause_webdriver(duration):
    """Puts webdriver to sleep for input amount of time. Used to give time for webpage to load elements - reducing "no such element" errors"""
    time.sleep(duration)

def login():
    """
    Carries out initial login process, calls methods to input login information(input_text) & select login buttons(click_element). 
    Calls duo_auth method to handle dual factor authentication when finished with login.
    """  
    click_element(find_element_Selector('#login-form > a > button'))
    input_text(find_element_Selector('#username'), "<YOUR USERNAME>")
    input_text(find_element_Selector('#password'), "<YOUR PASSWORD>")
    click_element(find_element_Selector('body > div > div > div > div.section.login > form > div.form-element-wrapper.mt-4 > button'))

def duo_authentication():
    """
    Switches driver frame to duo mobile iframe, allowing for interaction with present elements.
    Selects button to send mobile authentication confirmation and remember program.
    """
    frame = driver.find_element(By.ID, 'duo_iframe')
    driver.switch_to.frame(frame)
    click_element(WebDriverWait(driver, 20).until(EC.element_to_be_clickable(find_element_Selector('#login-form > div:nth-child(17) > div > label > input[type=checkbox]'))))                                
    click_element(find_element_Selector('#auth_methods > fieldset > div.row-label.push-label > button'))
    
    #Makes driver idle for 5 seconds to allow time for mobile authentication by hand
    pause_webdriver(8)

def permissions_popup():
    """Changes frame back from duo_iframe to default. Then accepts permissions request popup."""
    driver.switch_to.default_content()
    click_element(WebDriverWait(driver, 20).until(EC.element_to_be_clickable(find_element_Selector('body > form > div > div:nth-child(4) > p:nth-child(3) > input[type=submit]:nth-child(2)'))))

def course_page():
    pause_webdriver(1)
    click_element(WebDriverWait(driver, 20).until(EC.element_to_be_clickable(find_element_Selector('#base_tools > bb-base-navigation-button:nth-child(4) > div > li > a > ng-switch > div'))))#'#main-content-inner > div > header > section > button > bb-svg-icon'))
    #click_element(find_element_Selector('#base_tools > bb-base-navigation-button:nth-child(4) > div > li > a'))
    pause_webdriver(2)

def navigate_to_grades(course_element, my_grades_selector):
    """Navigates to each individual course's grade page from courses page."""
    try:
        pause_webdriver(2)
        click_element(WebDriverWait(driver, 20).until(EC.element_to_be_clickable(find_element_Selector(course_element))))
    except NoSuchElementException:
        print("DIDN'T FIND COURSE")
    pause_webdriver(3)
    try:
        frame = driver.find_element(By.NAME, 'classic-learn-iframe')
        driver.switch_to.frame(frame)
        click_element(WebDriverWait(driver, 20).until(EC.element_to_be_clickable(find_element_Selector(my_grades_selector)))) 
    except NoSuchElementException:
        print("Element not found")
    pause_webdriver(2)
    driver.execute_script("window.history.go(-2)")
    
    '''
    driver.switch_to.default_content()
    pause_webdriver(0.5)
    click_element(WebDriverWait(driver, 20).until(EC.element_to_be_clickable(find_element_Selector('#main-content-inner > div > header > section > button > bb-svg-icon'))))
    pause_webdriver(0.5)
    click_element(WebDriverWait(driver, 20).until(EC.element_to_be_clickable(find_element_Selector('#base_tools > bb-base-navigation-button:nth-child(8) > div > li > a > ng-switch > div > span'))))
    grade_scrape()
    '''

def grade_scrape():
    pause_webdriver(0.5)
    driver.switch_to.default_content()
    driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL, Keys.END) #Scrolls to elements in focus


def main():
    login()
    duo_authentication()
    permissions_popup()
    course_page()
    for course in course_dict:
        navigate_to_grades(course_dict[course][0], course_dict[course][1])
        pause_webdriver(0.5)

main()
driver.quit()
