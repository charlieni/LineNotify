from selenium.webdriver.common.by import By
from datetime import datetime
from webDriver import ChromeDriver
import time
global DIC
DIC = {}

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
        time.sleep(2)
        script = script.replace('openWindow','openWindowAction').replace('this.form', 'document.fm_t05sr01_1') # magic method
        #print(script)
        driver.execute_script(script)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)
        # save newData
        driver.get_screenshot_as_file('./screen.png')
        newData[key] = {
          #  'png': png,
            'source': driver.page_source
        }
        driver.close()
        driver.switch_to.window(baseWindow)
    print('job end at', datetime.now())
    return newData


if __name__ == '__main__':
    
    driver = ChromeDriver().driver
    dic=dict()
    dic=crawl(driver)
    print(dic.keys())
