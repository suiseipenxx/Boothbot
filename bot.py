from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#輸入區
url=""#搶購商品網址
account=""#pixiv賬號
password=""#pixiv密碼

#優化程式
options = Options()
options.add_argument('--no-sandbox')#最高權限
#options.add_argument('--headless')#不顯示瀏覽器和執行過程，Linux不支援可視化，所以一定要加
options.add_argument('--disable-javascript')#禁用JavaScript
options.add_argument('blink-settings=imagesEnabled=false')#不加載圖片
options.add_argument('--disable-software-rasterizer')#禁用渲染
options.add_argument('--disable-notifications')#禁用通知
options.add_argument('--disk-cache-dir=/path/to/cache')#讀取瀏覽器暫存
options.add_argument('--disable-gpu')#禁用使用內顯

options.add_argument('utf-8')#設定語言和編碼方式



driver = webdriver.Chrome(options)
driver.maximize_window()

#操作部分
driver.get(url)#搶購商品頁面 Purchasing Product Page


driver.find_element(By.XPATH,'/html/body/header/div/div/nav/div[2]/div[1]/a').click()# 到登入頁面Redirecting to the login page

driver.find_element(By.XPATH,'/html/body/div[2]/main/div[2]/div/div[1]/a').click()#登入pixiv Login to pixiv

#pixiv登入資料
driver.find_element(By.XPATH,'//*[@id="app-mount-point"]/div/div[3]/div[1]/div[3]/div/div/div/form/fieldset[1]/label/input').send_keys(account) # 輸入帳號
driver.find_element(By.XPATH,'//*[@id="app-mount-point"]/div/div[3]/div[1]/div[3]/div/div/div/form/fieldset[2]/label/input').send_keys(password) # 輸入密碼
driver.find_element(By.XPATH,'//*[@id="app-mount-point"]/div/div[3]/div[1]/div[3]/div/div/div/form/button').click()

time.sleep(2)

while 1:
    try:
        buy = WebDriverWait(driver, 1, 0.1).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[class='cmd-label']"))) # 顯性等待
        buy.click() # 偵測到可以購買按鈕就點擊按鈕
        print ("可以購買!")
        driver.find_element(By.XPATH,'//*[@id="js-carts-index"]/div[1]/div/div[4]/a[1]').click()#結賬付款
        driver.find_element(By.XPATH,'//*[@id="new_order"]/div[2]/label[1]/div/div/div[3]/div/input').click()#確認支付方式
        driver.find_element(By.XPATH,'//*[@id="persist"]/div/form/div/button').click()#確認收貨地點
        driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div/div[6]/form/div/input').click()#確認訂單 
        print ("購買完成")
        break
    except:
        print("還不能購買! 重新整理!")
        driver.refresh() # 重整頁面






