from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import recognize_local
import re
import emailto_u


def isElementExist():
    flag = False
    try:
        browser.find_element_by_xpath('//*[@id="2400000G790F"]')  # G79班次的ID，如果出现则说明有票,其他班次需改动
        return flag
    except:
        flag = True
        return flag


browser=webdriver.Chrome()
browser.get("https://www.ticketing.highspeed.mtr.com.hk/its/?lang=zh_HK")

browser.find_element_by_name("departStationName").click()#点击出发城市输入框
sleep(0.5)
browser.find_element_by_xpath("//ul[@id=\"ul_list1\"]/li[19]").click()#郑州东

browser.find_element_by_name("arriveStationName").click()#点击到达城市输入框
sleep(0.5)
browser.find_element_by_xpath("//ul[@id=\"ul_list1\"]/li[1]").click()#香港西九龙

js = "document.getElementById('departDate').removeAttribute('readonly')"   # jQuery，移除readonly
browser.execute_script(js)
browser.find_element_by_id("departDate").clear()
browser.find_element_by_id('departDate').send_keys('2019-02-10')#出发时间
sleep(0.5)

js_down="var q=document.documentElement.scrollTop=450"
browser.execute_script(js_down)#页面滑到最底部

browser.maximize_window()



sleep(0.2)
browser.find_element_by_id('captcha').click()
def captcha_break():
        browser.get_screenshot_as_file('screenshot.png')#截图
        imgelement = browser.find_element_by_xpath('//*[@id="kaptchaImage"]')  # 定位验证码
        location = imgelement.location  # 获取验证码x,y轴坐标
        size = imgelement.size  # 获取验证码的长宽
        rangle = (int(320), int(766), int(435),int(805))  # 写成我们需要截取的位置坐标(不同屏幕不同分辨率可能会有差异)
        i= Image.open("screenshot.png")  # 打开截图
        frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
        frame4= frame4.resize((90,30),Image.ANTIALIAS)#更改像素（训练模型为此像素）
        frame4 =frame4.convert('RGB')#转换为JPG
        frame4.save('save.jpg')
        p_text=recognize_local.main()#调用识别验证码程序
        browser.find_element_by_id('captcha').send_keys(p_text)#输入验证码
        sleep(0.5)
# 判断alert弹出框

captcha_break()
browser.find_element_by_id('query_btn').click()#提交验证码
pd=isElementExist()
sleep(1)
while pd:
        try:
                t=browser.find_element_by_id("alertMsg").get_attribute('textContent')
                print(t)
                sleep(3)
                browser.find_element_by_xpath('//*[@id="btsok"]').click()             
                captcha_break()
                browser.find_element_by_id('query_btn').click()#提交验证码
                pd=isElementExist()

        except:
                browser.find_element_by_id('query_btn').click()  # 提交验证码
                try:
                    sleep(3)
                    browser.find_element_by_xpath('//*[@id="btsok"]').click()
                    captcha_break()
                    browser.find_element_by_id('query_btn').click()  # 提交验证码
                except:
                    browser.find_element_by_id('captcha').clear()
                    browser.find_element_by_xpath('//*[@id="kaptchaImage"]').click()
                    captcha_break()
                    browser.find_element_by_id('query_btn').click()#提交验证码
                pd=isElementExist()

else:
                browser.maximize_window()
                browser.execute_script("window.scrollBy(10,-500)")
                sleep(2)
                browser.find_element_by_xpath('//*[@id="2400000G790F"]').click()
                sleep(0.5)
                browser.find_element_by_xpath('//*[@id="query_list"]/tr[2]/td[8]/a/img').click()
                print("有票")
                emailto_u()  #发邮件
