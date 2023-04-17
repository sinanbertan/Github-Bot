#İmporting libraries:
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.common.by import By 
from user import username, password #importing username and password from self created user.py file


class Github_Bot:
    #using chrome driver:
    chrome_driver_path="D:\Drivers\chromedriver_win32\chromedriver.exe"
    
    def __init__(self):
        self.browser=webdriver.Chrome(Github_Bot.chrome_driver_path)
        self.base_url="https://github.com/"
        self.username=username
        self.password=password
        self.followers=[]
        
    def login(self):
        self.browser.get(self.base_url+"login")
        nameInput=self.browser.find_element(By.NAME,"login")
        passwordInput=self.browser.find_element(By.NAME,"password")
        button=self.browser.find_element(By.NAME,"commit")
        
        nameInput.send_keys(self.username[0])
        nameInput.send_keys(Keys.TAB)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.TAB)
        button.click()
    
    def get_repos(self,syc):
        repos=self.browser.find_element(By.NAME,"q")
        repos.send_keys("python")
        repos.send_keys(Keys.ENTER)

        
        while syc>0:
            repo1=self.browser.find_elements(By.CSS_SELECTOR,".repo-list-item")
            syc-=1
            for repo in repo1:
            
                next_page=self.browser.find_element(By.CSS_SELECTOR,".next_page")
                anc=repo.find_elements(By.TAG_NAME,"a")[0]
                prg=repo.find_elements(By.TAG_NAME,"p")[0]
                rName=anc.text
                rLink=anc.get_attribute("href")
                dsc=prg.text
                print(f"Repo Name: {rName}, Repo Link: {rLink}, Description: {dsc}")
                next_page.click()
                
    def loadFollowers(self):
        items = self.browser.find_elements(By.CSS_SELECTOR,'.d-table.table-fixed')

        for item in items:
            name = item.find_elements(By.TAG_NAME,'div')[1].find_elements(By.TAG_NAME,'span')[0].text
            username = item.find_elements(By.TAG_NAME,'div')[1].find_elements(By.TAG_NAME,'span')[1].text
            user = {
                "name": name,
                "username": username
            }
            self.followers.append(user)

    def getFollowers(self):
        self.browser.get(f"{self.base_url}{self.username[1]}?tab=followers")
        self.loadFollowers()        

        while True:
            links = self.browser.find_element(By.CLASS_NAME,'pagination').find_elements(By.TAG_NAME,'a')

            if len(links) == 1:
                if links[0].text == "Next":
                    links[0].click()
                    self.loadFollowers() 
                else:
                    break
            else:
                for link in links:
                    if  link.text == "Next":
                        link.click()
                        self.loadFollowers()
                    else:
                        continue
                    
        print(self.followers)
        print(len(self.followers))      
    
    def __del__(self):
        time.sleep(4)
        self.browser.close()
        
        
var=Github_Bot()
print("""
      -> 1. Login
      -> 2. Get Repos
      -> 3. Get Followers
      -> 4. Exit\n\n
      """)

slc=int(input("Please select an option: "))
while True:
    if slc==1:
        var.login()
        break
    elif slc==2:
        sy=int(input("Please enter the number of pages you want to see: "))
        var.get_repos(sy)
        break
    elif slc==3:
        var.getFollowers()
        break
    elif slc==4:
        print("Exiting...")
        break
    

    