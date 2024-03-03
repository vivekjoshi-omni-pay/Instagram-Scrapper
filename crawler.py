from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import requests

# Set your Instagram username and password
username = "xxx"
password = "xxxx"
profile_to_scrape = "_pragyasree"  # Replace with the desired profile username

imageUrl = set()

driver = webdriver.Firefox()

# Open Instagram and log in
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(2)

# Find the username field by searching for an input field within the login form
login_form = driver.find_element(By.ID, "loginForm")
username_field = login_form.find_element(By.NAME, "username")
password_field = login_form.find_element(By.NAME, "password")

# Fill in the username and password fields
username_field.send_keys(username)
password_field.send_keys(password)

# Press Enter to log in
password_field.send_keys(Keys.RETURN)

# Wait for the login process to complete
time.sleep(5)

# Go to the user's profile
profile_url = f"https://www.instagram.com/{profile_to_scrape}/"
driver.get(profile_url)
time.sleep(5)

# last_height = driver.execute_script("return document.body.scrollHeight")

# while True:
#     # Scroll down to trigger more content loading
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
#     # Wait for some time to let new content load
#     time.sleep(2)

#     # Calculate new scroll height and compare with the last scroll height
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break  # If no more data is loaded, exit the loop
#     last_height = new_height

def getCurrentHeight(browser):
    return browser.execute_script("return document.body.scrollHeight")


def scrollPage(browser, totalHeight):
    for i in range(0, totalHeight, 500):
        time.sleep(0.5)
        browser.execute_script(f"window.scrollTo({i}, {i+500});")
    browser.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    
def scroll(browser):
    initialHeight = int(getCurrentHeight(browser))
    scrollPage(browser,initialHeight)
    currentHeight = int(getCurrentHeight(browser))
    while(initialHeight!=currentHeight):
        print(initialHeight, currentHeight)
        scrollPage(browser,currentHeight)
        initialHeight = currentHeight
        currentHeight = int(getCurrentHeight(browser))
        main_container = driver.find_elements(By.XPATH, '//main')[0]
        header_container = main_container.find_elements(By.XPATH, '//header')[0]
        parent_container = header_container.find_elements(By.XPATH, '../..')[0]
        div_container = parent_container.find_elements(By.XPATH, '//div')[-1]
        image_containers = div_container.find_elements(By.XPATH,'//img')
        print("length of", len(image_containers))
        for i, post_element in enumerate(image_containers):
            class_attribute_value = post_element.get_attribute('src')
            print(f"Image URL for post {i+1}: {class_attribute_value}")
            imageUrl.add(class_attribute_value)
        

scroll(driver)
# main_container = driver.find_elements(By.XPATH, '//main')[0]
# header_container = main_container.find_elements(By.XPATH, '//header')[0]
# parent_container = header_container.find_elements(By.XPATH, '../..')[0]
# div_container = parent_container.find_elements(By.XPATH, '//div')[-1]
# image_containers = div_container.find_elements(By.XPATH,'//img')
# print("length of", len(image_containers))


with open("url.text", "w+") as file:
    
    for i, post_element in enumerate(imageUrl):
        
        # Print image URL
        # class_attribute_value = post_element.get_attribute('src')
        
        # print(f"Image URL for post {i+1}: {class_attribute_value}")
        file.write(post_element + '\n')
# image_elements = driver.find_elements(By.XPATH, '//img[@class="x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3"]')
# post_elements = driver.find_elements(By.XPATH, '//div[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd"]')
# print("Post elements", image_elements)

# # Create a folder to save all the images
# all_images_folder = os.path.join(profile_to_scrape, "all_images")
# if not os.path.exists(all_images_folder):
#     os.makedirs(all_images_folder)
    

# for i, post_element in enumerate(image_elements):
    
#     # Print image URL
#     class_attribute_value = post_element.get_attribute('src')
#     print(f"Image URL for post {i+1}: {class_attribute_value}")

#     # # Download image
#     # response = requests.get(class_attribute_value)
#     # with open(os.path.join(all_images_folder, f"image_{i+1}.jpg"), 'wb') as f:
#     #     f.write(response.content)

#     # Go back to the user's profile
#     time.sleep(2)

# Quit the driver
input("Enter to exit the application")
driver.quit()