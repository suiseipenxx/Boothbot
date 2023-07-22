from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from retrying import retry
import requests
import time
import sys

#輸入區
url = ""  # 搶購商品網址
account = ""  # pixiv賬號
password = ""  # pixiv密碼

#優化
@retry(wait_fixed=2, stop_max_attempt_number=1)
def send(path,ap):
    driver.find_element(By.CSS_SELECTOR,path).send_keys(ap)

def click(path):
    driver.find_element(By.CSS_SELECTOR,path).click()

#瀏覽器選項
options = Options()
#options.add_argument('--headless')#無頭模式
options.add_argument('--window-size=1920,1080')#設定視窗大小，開啟無頭模式情況下一定要有，不然會抓不到元素
options.add_argument('--start-maximized')

options.add_argument('--log-level=1')#設定log等級，不然會有很多log顯示
options.add_argument('--no-sandbox')#最高權限
options.add_argument('--blink-settings=imagesEnabled=false')#不加載圖片
options.add_argument('--disable-software-rasterizer')#禁用渲染
options.add_argument('--disable-notifications')#禁用通知
options.add_argument('--disable-gpu')#禁用使用內顯
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--disable-plugins')
options.add_argument('--disable-popup-blocking')
options.page_load_strategy='none'

#反爬蟲
headers= {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
    "Accept-Encoding": "gzip, deflate, br", 
    "Accept-Language": "zh-TW,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5", 
    "Host": "booth.pm/zh-tw", 
    "Referer": "https://www.google.com/", 
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"", 
    "Sec-Ch-Ua-Mobile": "?0", 
    "Sec-Ch-Ua-Platform": "\"Windows\"", 
    "Sec-Fetch-Dest": "document", 
    "Sec-Fetch-Mode": "navigate", 
    "Sec-Fetch-Site": "cross-site", 
    "Sec-Fetch-User": "?1", 
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36", 
    "X-Amzn-Trace-Id": "Root=1-64bb6ed9-0161b8da3a92673d3abed8f8"
}
options.add_argument('--user-agent={headers["User-Agent"]}')
options.add_argument('--accept-language={headers["Accept-Language"]}')

driver = webdriver.Chrome(options)
driver.maximize_window()


driver.get(url)#搶購商品頁面 Purchasing Product Page
driver.implicitly_wait(4)
click('[href="/users/sign_in"]')
click('[class="btn pixiv-oauth signin full-length"]')
print('登入中')

#pixiv登入資料
driver.implicitly_wait(4)
send('[class="sc-bn9ph6-6 degQSE"]',account)
send('[class="sc-bn9ph6-6 hfoSmp"]',password)
click('[class="sc-bdnxRM jvCTkj sc-dlnjwi klNrDe sc-2o1uwj-6 NmyKg sc-2o1uwj-6 NmyKg"]')
print('登入成功')

driver.get(url)

locators=(By.CSS_SELECTOR,'[class="btn add-cart full-length"]')#等待的條件
print('搶商品中')

while 1:
    try:
        buy = WebDriverWait(driver, 3, 0.1).until(EC.presence_of_element_located(locators)) # 顯性等待
        buy.click() # 偵測到可以購買按鈕就點擊按鈕
        print("開始結賬")
        click('[class="btn btn--primary u-w-sp-100"]')
        print("確認付款方式")
        click('[name="commit"]')
        print("確認送貨地址")
        click('[name="button"]')
        print("購買")
        #click('[name="commit"]')
        print ("購買完成")
        driver.quit()
        break
    except:
        driver.save_screenshot('screenshot.png')
        driver.refresh() # 重整頁面
        print("刷新")
