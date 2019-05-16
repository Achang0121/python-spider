import json
import time
from scrapy.http import HtmlResponse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException


results = []
# 解析页面所需要的信息
def parse(response):
    for comment in response.css('div.comment-item'):
        result = {}
        result['name'] = comment.xpath('.//div[@class="user-name"]/a/text()').extract_first().strip()
        result['content'] = comment.xpath('.//div[@class="content"]/text()').extract_first().strip()
        results.append(result)


# 判断是否有下一页
def has_next_page(response):
    flag = response.xpath('//ul[@class="pagination"]/li[2]/@class').extract_first()
    if 'disabled' in flag:
        return False
    else:
        return True

# 跳转下一页
def goto_next_page(driver):
    try: 
        driver.find_element_by_xpath('//ul[@class="pagination"]/li[2]/a').click()
    except ElementClickInterceptedException:
        return False


# 显式等待，这里没有用上
def wait_page_return(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//ul[@class="pagination"]/li[2]')
        )    
    )

def spider():
    driver = webdriver.Chrome()
    url = 'https://www.shiyanlou.com/courses/427'
    driver.get(url)
    while True:
        #wait_page_return(driver)
        driver.implicitly_wait(5)  # 这里不使用显示等待，隐式等待 5 秒
        html = driver.page_source
        response = HtmlResponse(url=url, body=html.encode('utf8'))
        parse(response)
        if not has_next_page(response):
            break
    
        time.sleep(3)
        goto_next_page(driver)
        
    with open('/home/shiyanlou/comments.json', 'w') as f:
        f.write(json.dumps(results))
    driver.close()

if __name__ == '__main__':
    spider()
