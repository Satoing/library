from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import datetime

# 填写信息
uname = ''
pword = ''

room1 = 'A-S320'
room2 = 'A-S321'
wants = ['A-S321', 'A-S320', 'A-S324', 'A-S325', 'A-S341', 'A-S342', 'A-S343', 'A-S344']
start = '800'
end = '2130' #图书馆改版后最多只能约4个小时，算一下起始时间

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(chrome_options=options)

driver.set_window_size(1366,768)

driver.get('https://idas-uestc-edu-cn.vpn.uestc.edu.cn:8118/authserver/login?service=https%3A%2F%2Fvpn.uestc.edu.cn%2Fauth%2Fcas_validate%3Fentry_id%3D1')

time.sleep(3)

print("登录easyconnect")
driver.save_screenshot('result1.png')
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(uname)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(pword)
driver.find_element(By.XPATH, '//*[@id="login_submit"]').click()
time.sleep(5)

print("登录图书馆")
driver.get('https://reservelib-uestc-edu-cn.vpn.uestc.edu.cn:8118/clientweb/xcus/ic2/Default.aspx')
time.sleep(5)
driver.save_screenshot('result2.png')

d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date())+'6:31', '%Y-%m-%d%H:%M')
while True:
    n_time = datetime.datetime.now()
    # 判断当前时间是否到6点半
    if n_time > d_time1: break

def reserve(myroom):
    driver.find_element(By.XPATH, f'//*[@id="item_list"]/ul/li[8]/ul/li[4]').click()
    time.sleep(3)

    today = datetime.datetime.now ().weekday ()
    if today == 6:
        driver.find_element(By.CSS_SELECTOR, '.cld-h-bt-next').click()
    else:
        driver.find_element(By.XPATH, f'.//*[@class="cld-h-row"]/td[@index="{(today+1)}"]').click()

    time.sleep(3)
    # 向下滚动
    js="var q=document.documentElement.scrollTop=1000000" 
    driver.execute_script(js)
    js="var q=document.documentElement.scrollTop=1000000" 
    driver.execute_script(js)
    js="var q=document.documentElement.scrollTop=1000000" 
    driver.execute_script(js)
    js="var q=document.documentElement.scrollTop=1000000" 
    driver.execute_script(js)
    js="var q=document.documentElement.scrollTop=1000000" 
    driver.execute_script(js)

    driver.find_element(By.XPATH, f'.//*[@class="cld-list-qzs"]/div[@objname="{myroom}"]/table/tbody/tr/td[16]').click()
    time.sleep(1)
    driver.save_screenshot('result4.png')

    element = driver.find_element(By.XPATH, '//*[@id="resv_kind"]')
    driver.execute_script("arguments[0].click()", element)
    driver.save_screenshot('result5.png')
    driver.find_element(By.XPATH, '//*[@id="resv_kind"]/option[2]').click()

    element = driver.find_element(By.XPATH, '//form/div[1]/table/tbody[2]/tr[2]/td[2]/div/span[1]/select[1]')
    driver.execute_script("arguments[0].click()", element)
    
    # 检查开始时间是否符合预期
    earlist = driver.find_elements(By.CSS_SELECTOR, '.mt_start_time option')[0].text
    hour=int(earlist.split(':')[0])
    if hour > 8: start0 = '930'
    else: start0 = start

    driver.find_element(By.XPATH, f'//form/div[1]/table/tbody[2]/tr[2]/td[2]/div/span[1]/select[1]/option[@value="{start0}"]').click()

    element = driver.find_element(By.XPATH, '//form/div[1]/table/tbody[2]/tr[2]/td[2]/div/span[3]/select')
    driver.execute_script("arguments[0].click()", element)
    driver.find_elements(By.CSS_SELECTOR, '.mt_end_time option')[-1].click()

    driver.find_element(By.XPATH, '//form/div[@class="submitarea"]/input[1]').click()
    return True

today = datetime.datetime.now ().weekday ()

if today % 2 == 0: room = room1
else: room = room2

print("开始预约")
try: 
    reserve(room)
    exit(0)
except: 
    for want in wants:
        if want == room: continue
        driver.get('http://reservelib-uestc-edu-cn.vpn.uestc.edu.cn:8118/clientweb/xcus/ic2/Default.aspx')
        time.sleep(3)
        try: 
            if reserve(want):
                exit(0)
        except: continue


time.sleep(5)
driver.save_screenshot('result.png')
