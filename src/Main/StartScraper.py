import asyncio
import os
from src.Main.LoginAccount import LoginAccount
from src.Utility.BrowserUtility import BrowserUtility
from src.Utility.OSUtility import OSUtility
from src.Logging.Logger import Logger
from src.Main.MailNotify import MailNotify
from selenium.webdriver.common.by import By


class StartScraper:
    def __init__(self):
        self.logger = None
        self.mailNotify = MailNotify()
        self.osUtils = None
        self.configJson = None
        self.imageUrls = set()


    def start(self, configJson):
        self.logger = Logger(configJson, "StartScraper").logger
        self.logger.info("""StartScraper Initiated...
                            To Terminate, Click on Stop ScraperType Button
                        """)
        self.osUtils = OSUtility(configJson)
        self.browserUtils = BrowserUtility(configJson)
        self.loginUtils = LoginAccount(configJson)
        self.configJson = configJson
        try:
            username = configJson["username"]
            self.logger.info(f"Started Scraping for Username: {username}")
            self.browser = self.browserUtils.loadBrowser()
            self.browser.get(f"https://www.instagram.com/{username}/")
            self.osUtils.sleep(5)
            self.loginUtils.browser = self.browser
            self.loginUtils.checkIfLoggedIn()
            self.customScrollAndScrapeData()
            self.saveImageUrls()
            asyncio.get_event_loop().run_until_complete(self.browserUtils.shutdownChromeViaWebsocket())
            self.mailNotify.send_email("Scraping Complete")
        except KeyboardInterrupt:
            self.logger.error("Keyboard Interrupt")
        except Exception as e:
            lineNumber = e.__traceback__.tb_lineno
            self.logger.error(f"start: {lineNumber}: {e}")
            asyncio.get_event_loop().run_until_complete(self.browserUtils.shutdownChromeViaWebsocket())
            self.mailNotify.send_email(f"Exception occured in line number {lineNumber}, {e}")
        finally:
            self.logger.debug("Exiting Scraper...")


    def getCurrentHeight(self):
        self.logger.info("Getting Current Height")
        return self.browser.execute_script("return document.body.scrollHeight")


    def scrollPage(self, totalHeight):
        self.logger.info("Scrolling Page")
        for i in range(0, totalHeight, 500):
            self.osUtils.sleep(0.5)
            self.browser.execute_script(f"window.scrollTo({i}, {i+500});")
        self.browser.execute_script("window.scrollTo(0, 0);")
        self.osUtils.sleep(2)
        

    def customScrollAndScrapeData(self):
        self.logger.info("Scrolling Page")
        initialHeight = int(self.getCurrentHeight())
        self.scrollPage(initialHeight)
        currentHeight = int(self.getCurrentHeight())
        while(initialHeight!=currentHeight):
            print(initialHeight, currentHeight)
            self.scrollPage(currentHeight)
            initialHeight = currentHeight
            currentHeight = int(self.getCurrentHeight())
            mainContainer = self.browser.find_elements(By.XPATH, '//main')[0]
            headerContainer = mainContainer.find_elements(By.XPATH, '//header')[0]
            parentContainer = headerContainer.find_elements(By.XPATH, '../..')[0]
            divContainer = parentContainer.find_elements(By.XPATH, '//div')[-1]
            imageContainers = divContainer.find_elements(By.XPATH,'//img')
            self.logger.info(f"length of {len(imageContainers)}")
            for i, imageTag in enumerate(imageContainers):
                imgUrl = imageTag.get_attribute('src')
                self.logger.debug(f"Image URL for post {i+1}: {imgUrl}")
                self.imageUrls.add(imgUrl)
    

    def saveImageUrls(self):
        self.logger.info("Saving Image URLs to file")
        textFilePath = os.path.join(self.configJson["saveDirectory"], "ImageUrls.txt")
        with open(textFilePath, "w+") as file:
            for i, url in enumerate(self.imageUrls):
                file.write(f"{url}\n")