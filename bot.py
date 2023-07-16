from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from retrying import retry
import sys

#輸入區
url=""#搶購商品網址
account=""#pixiv賬號
password=""#pixiv密碼

#優化
@retry(wait_fixed=2, stop_max_attempt_number=1)
def send(path,ap):
    driver.find_element(By.CSS_SELECTOR,path).send_keys(ap)
def click(path):
    driver.find_element(By.CSS_SELECTOR,path).click()

#瀏覽器選項
options = Options()
options.page_load_strategy='none'
options.add_argument('--headless')#無頭模式
options.add_argument('--window-size=1920,1080')#設定視窗大小，開啟無頭模式情況下一定要有，不然會抓不到元素
options.add_argument('--start-maximized')
options.add_argument('--log-level=2')#設定log等級，不然會有很多log顯示
options.add_argument('--no-sandbox')#最高權限
options.add_argument('--disable-javascript')#禁用JavaScript
options.add_argument('--blink-settings=imagesEnabled=false')#不加載圖片
options.add_argument('--disable-software-rasterizer')#禁用渲染
options.add_argument('--disable-notifications')#禁用通知
options.add_argument('--disk-cache-dir=/path/to/cache')#讀取瀏覽器暫存
options.add_argument('--disable-gpu')#禁用使用內顯
options.add_argument("--disable-extensions")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(options)
driver.maximize_window()


#操作部分
driver.get(url)#搶購商品頁面 Purchasing Product Page
driver.implicitly_wait(2)#隱形等待
click('[href="/users/sign_in"]')
click('[class="btn pixiv-oauth signin full-length"]')
print('登入中')
#pixiv登入資料
driver.implicitly_wait(2)#隱形等待
send('[class="sc-bn9ph6-6 degQSE"]',account)
send('[class="sc-bn9ph6-6 hfoSmp"]',password)
click('[class="sc-bdnxRM jvCTkj sc-dlnjwi klNrDe sc-2o1uwj-6 NmyKg sc-2o1uwj-6 NmyKg"]')
print('登入成功')

locators=(By.CSS_SELECTOR,'[class="btn add-cart full-length"]')#等待的條件
print('搶商品中')
while 1:
    try:
        buy = WebDriverWait(driver, 0.5, 0.1).until(EC.presence_of_element_located(locators)) # 顯性等待
        buy.click() # 偵測到可以購買按鈕就點擊按鈕
        click('[class="btn btn--primary u-w-sp-100"]')
        click('[name="commit"]')
        click('[name="button"]')
        #click('[name="commit"]')
        print ("購買完成")
        driver.quit()
        sys.exit("結束程式")
    except:
        driver.refresh() # 重整頁面






