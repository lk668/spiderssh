#!/usr/bin/python
# -*- coding: utf-8 -*-


from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from ssh.items import SshItem


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import time


class SshSpider(Spider):
    
    name = 'sshspider'

    #减慢爬取速度为 0.5s
    download_delay = 0.5
    allowed_domains = ['boafanx.tabboa.com'] #可以不写

    start_urls = ["http://boafanx.tabboa.com/free"]

    def parse(self, response):
        
        sel = Selector(response)
        ssh = sel.xpath('//pre/code/text()').extract()

        item = SshItem()
        item['ssh'] = ssh[1].encode('utf-8')
        s = ''
        for i in range(28,33):
            s += str(ord(ssh[1][i])-9311)
        item['port'] = s
        yield item
        login("admin", item['port'])


def login(username, port):
    browser = webdriver.Firefox()
    browser.get("http://192.168.199.1/login_web.html")
    wait = ui.WebDriverWait(browser, 20)

    user = browser.find_element_by_xpath("//div[@id = 'loginbox']/form[@id = 'loginform']/input[@id = 'input_password1']")
    user.clear()
    user.send_keys(username, Keys.ARROW_DOWN)

    browser.find_element_by_xpath("//div[@id = 'loginbox']/form[@id = 'loginform']/input[@id = 'submit_btn']").click()

    wait.until(lambda browser: browser.find_element_by_xpath("//div[@id = 'content']/div[@class = 'wrap']/div[@id = 'main']\
        /div[@id = 'services']/a/span[@class = 'txt']"))
    browser.find_element_by_xpath("//div[@id = 'content']/div[@class = 'wrap']/div[@id = 'main']/div[@id = 'services']\
        /a/span[@class = 'txt']").click()
    print browser.window_handles
    browser.switch_to_window(browser.window_handles[1])
    wait.until(lambda browser: browser.find_element_by_xpath("//div[@class = 'g-app-list']/ul[@class = 'clearfix']/li"))

    browser.find_element_by_xpath("//div[@class = 'g-app-list']/ul[@class = 'clearfix']/li/a[@href = 'store.php?m=plugins&a=info&rid=r838112254&sid=19']").click()

    wait.until(lambda browser: browser.find_element_by_xpath("//div[@class = 'info']/div[@class = 'detail-msg']/div[@class = 'sub-tab']\
        /a[@id = 'p_config']"))
    browser.find_element_by_xpath("//div[@class = 'info']/div[@class = 'detail-msg']/div[@class = 'sub-tab']\
        /a[@id = 'p_config']").click()
    print "$$$$$$$$$$$$$$$"
    portnum = browser.find_element_by_xpath("//tbody/tr[2]/td/input[@class = 'txt']")
    portnum.clear()
    portnum.send_keys(port, Keys.ARROW_DOWN)

    time.sleep(3)
    button = browser.find_element_by_xpath("//input[@id = 'saveconfig2']").click()

    time.sleep(10)
    browser.find_element_by_xpath("//a[@id = 'b_url']").click()

    wait.until(lambda browser: browser.find_element_by_xpath("//input[@id = 'refresh']"))
    for i in range(10):
        browser.find_element_by_xpath("//input[@id = 'refresh']").click()
        time.sleep(2)
        data = browser.find_element_by_tag_name("font").text
        if data.encode('utf-8') == "运行中":
            break
