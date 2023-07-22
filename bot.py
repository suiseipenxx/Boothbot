from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from retrying import retry
import requests
import time
import sys

#輸入區
url = ""  #搶購商品網址
account = ""  # pixiv賬號
password = ""  # pixiv密碼 
#優化
@retry(wait_fixed=1, stop_max_attempt_number=5)
def send(path,ap):
    driver.find_element(By.CSS_SELECTOR,path).send_keys(ap)

def click(path):
    driver.find_element(By.CSS_SELECTOR,path).click()

#瀏覽器選項
options = uc.ChromeOptions()
options.add_argument('--headless')#無頭模式
options.add_argument('--window-size=1920,1080')#設定視窗大小，開啟無頭模式情況下一定要有，不然會抓不到元素
options.add_argument('--start-maximized')
options.add_argument('--log-level=1')#設定log等級，不然會有很多log顯示
options.add_argument('--no-sandbox')#最高權限
options.add_argument('--blink-settings=imagesEnabled=false')#不加載圖片
options.add_argument('--disable-software-rasterizer')#禁用渲染
options.add_argument('--disable-notifications')#禁用通知
options.add_argument('--disable-gpu')#禁用使用內顯
options.add_argument("--disable-dev-shm-usage")#使用共用內存
options.add_argument('--disable-plugins')#禁用插件
options.add_argument('--disable-popup-blocking')#禁止跳出視窗
options.page_load_strategy='none'#網頁載入策略

#反反爬蟲
ua = UserAgent()
options.add_argument("--user-agent={}".format(ua.edge))
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)


#啟動
driver=uc.Chrome(headless=True,use_subprocess=True)
driver.maximize_window()



driver.get(url)#搶購商品頁面 Purchasing Product Page
driver.implicitly_wait(3)
click('[href="/users/sign_in"]')
click('[class="btn pixiv-oauth signin full-length"]')
print('登入中')

#pixiv登入資料
driver.implicitly_wait(2)
send('[class="sc-bn9ph6-6 degQSE"]',account)
send('[class="sc-bn9ph6-6 hfoSmp"]',password)
click('[class="sc-bdnxRM jvCTkj sc-dlnjwi klNrDe sc-2o1uwj-6 NmyKg sc-2o1uwj-6 NmyKg"]')
print('登入成功')

driver.implicitly_wait(3)
print('搶商品中')

try:
    while driver.find_element(By.CSS_SELECTOR,'[class="btn add-cart full-length disabled"]')!=None :
        driver.refresh() # 在 while 循環內刷新頁面
        time.sleep(1)
        print("刷新")
except:
    try:
        click('[class="btn add-cart full-length"]')
        print("開始結賬")
        click('[href="https://checkout.booth.pm/checkout/step1?uuid=77c6444b-e8fa-46d9-a5e2-6463c889a13b"]')
        print("確認付款方式")
        click('[name="commit"]')
        print("確認送貨地址")
        click('[name="button"]')
        print("購買")
        click('[name="commit"]')
        print("購買完成")
        driver.quit()
    except: 
        driver.refresh() # 在 while 循環內刷新頁面
        time.sleep(0.5)
        print("刷新")

        
