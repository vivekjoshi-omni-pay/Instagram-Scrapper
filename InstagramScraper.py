import ctypes
import platform

from src.Common.Constants import constants
from src.UI.HomeScreenGUI import HomeScreen
from src.Utility.ConfigUtility import ConfigUtility
from src.Utility.FileUtility import FileUtility


class InstagramScraper:
    def __init__(self):
        self.version = "v0.0.2 Dev Branch"
        print(f"""
                Instagram Scraper ({self.version}), developed by Vivek/Anilabha
                Project Link: https://github.com/vivekjoshi-omni-pay/Instagram-Scrapper
                Check out ReadMe for more information about this project.
                Use the GUI to start scraping.
        """)
        if platform.system() == "Windows":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("InstagramScraper")
        self.fileUtil = FileUtility()
        self.configUtil = ConfigUtility()
        self.loadBasicUtility()


    def loadBasicUtility(self):
        self.fileUtil.createFolderIfNotExists(constants.OS_ROOT)
        self.configUtil.createDefaultConfigIfNotExists()


    def run(self):
        HomeScreen(self.version).createHomeScreen()


if __name__ == '__main__':
    app = InstagramScraper()
    app.run()
