from selenium.webdriver.common.by import By
from datetime import datetime
from webDriver import ChromeDriver
import time
import requests
global DIC
DIC = {}
underlinelist={"減資","庫藏股","轉換","澄清","本公司召開","公司債","增資"}
urlline = 'https://notify-api.line.me/api/notify'
token = '4lRN30G7BsMNpV52kAYGj88xhpvdCx5Pm4r1fdgOzAK'   ###授權碼
headers = {
    'Authorization': 'Bearer ' + token    # 設定 LINE Notify 權杖
}

def crawl(driver):
    print('job start at', datetime.now())
    url = 'https://mops.twse.com.tw/mops/web/t05sr01_1'
    if driver.current_url == url:
        driver.refresh()
    else:
        driver.get(url)

    # find new events
    eventsTable = driver.find_element(By.XPATH, '//*[@id="table01"]/form[2]/table/tbody')
    trs = eventsTable.find_elements(By.TAG_NAME, 'tr')
    newEvenrs = {}
    for tr in trs:
        try:
            tds = tr.find_elements(By.TAG_NAME, 'td')
            key = ''
            for td in tds[:-1]:
                key+=td.text
                key+=' '
            if key in DIC.keys():
                continue
            else:
                DIC[key] = tds[-1].find_element(By.TAG_NAME, 'input').get_attribute('onclick')
                newEvenrs[key] = DIC[key]
        except:
            pass
    
    # excecute newEvenrs
    newData = {}
    baseWindow = driver.window_handles[0]
    for key, script in newEvenrs.items():
        script = script.replace('openWindow','openWindowAction').replace('this.form', 'document.fm_t05sr01_1') # magic method
        #print(script)
        driver.execute_script(script)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
        # save newData
        driver.get_screenshot_as_file('./screen.png')
        newData[key] = {
        #    'png': png,
            'source': driver.page_source
        }
        driver.close()
        driver.switch_to.window(baseWindow)
        ####判斷字詞發送notify
        for word in underlinelist:
            if word in key:
                message=''
                underline="【"+word+"】"
                cmpnynum="("+key[0:4]+")"
                count=0
                cmpnyname=''
                announcement=''
                for i in range(0,len(key)):
                    if key[i] ==' ' and count!=4:
                        count+=1
                    if count==1:
                        cmpnyname+=key[i]    
                    elif count == 4:
                        announcement+=key[i]
                message=underline+"\n"+cmpnynum+cmpnyname+"-重大消息"+"\n"+announcement
                image = open('./screen.png', 'rb')
                imageFile = {'imageFile' :image}   # 設定圖片資訊
                data = {
                'message':message ,     # 設定 LINE Notify message ( 不可少 )
                }
                data = requests.post(urlline, headers=headers, data=data, files=imageFile)   # 發送 LINE Notify
                break
    print('job end at', datetime.now())
    return newData
    
        

if __name__ == '__main__':
    
    pass
