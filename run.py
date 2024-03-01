import re
import requests
import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

cookie = {}
headers = {
        'User-Agent': '',
    }
well_stu = {} #存放将要学习的项目的连接

option = webdriver.ChromeOptions()
option.add_argument(r'--user-data-dir=')
browser = webdriver.Chrome(options=option)

news = []
obj = ['每日答题','每周答题','专项答题']
well_reading = []
cookies_list = []
video_list = []

def get_all_task():
    #该函数用于获得全部任务的详情
    all_task = 'https://pc-proxy-api.xuexi.cn/api/score/days/listScoreProgress?sence=score&deviceType=2'

    response = requests.get(all_task,headers=headers,cookies=cookie)
    content = json.loads(response.text)['data']
    # print(response.text)

    taskProgress = content['taskProgress']
    # print(taskProgress)

    for task in taskProgress:
        title = task['title']
        now = task['currentScore']
        max = task['dayMaxScore']
        if now == max:
            print(title,'已经满分')
        else:
            print(title,'满分：',max,'您获得了：',now,'分')
            well_stu[title] = task['guideUrl']
    print(well_stu)

def get_all_new():
    url = 'https://www.xuexi.cn/lgdata/3uoe1tg20en0.json'
    res = requests.get(url,headers=headers)

    content = json.loads(res.text)
    for item in content:
        news.append(item['url'])

def is_end():
    flag = True
    try:
        browser.find_element_by_xpath('//*[@id="page-footer"]')
    except Exception as error:
        flag = False
    finally:
        return flag

def reading():
    #阅读模块
    print('阅读模块')
    get_all_new() #找到所有的新闻地址放到列表中
    for i in range(12):
        well_reading.append(random.choice(news))

    browser.get('https://pc.xuexi.cn/points/my-points.html')
    time.sleep(3)
    for cookie in cookies_list:
        browser.add_cookie(cookie)

    for url in well_reading:
        browser.get(url)
        time.sleep(2)
        try:
            browser.find_element_by_class_name('voice-lang-switch').click()
        except:
            pass

        for i in range(8):
            browser.find_element_by_xpath('/html/body').send_keys(Keys.PAGE_DOWN)
            time.sleep(random.randint(1,3))
        time.sleep(random.randint(3,5))

    browser.get(random.choice(news))
    time.sleep(2)
    try:
        browser.find_element_by_class_name('voice-lang-switch').click()
    except:
        pass

    time.sleep(1)
    for i in range(2):
        browser.find_element_by_xpath('/html/body').send_keys(Keys.PAGE_DOWN)
    for i in range(6):
        time.sleep(60)

    print('选读文章结束')

def write(title):
    #答题模块
    print(title)


    if title=='每周答题':
        count = 86
        with open("config.ini",'r',encoding='utf-8') as file:
            subjected = file.readlines()
        for subject in subjected:
            if str(count)==subject.strip():
                count += 1

        with open('config.ini','a',encoding='utf-8') as f:
            f.write('\n')
            f.write(str(count))
        url = 'https://pc.xuexi.cn/points/exam-weekly-detail.html?id='+str(count)
        print(url)

        browser.get(url)
        time.sleep(100)

    elif title=='每日答题':
        browser.get('https://pc.xuexi.cn/points/exam-practice.html')
        time.sleep(100)

    elif title=='专项答题':
        count = 68
        with open("config2.ini", 'r', encoding='utf-8') as file:
            subjected = file.readlines()
        for subject in subjected:
            if str(count) == subject.strip():
                count += 1

        with open('config2.ini', 'a', encoding='utf-8') as f:
            f.write('\n')
            f.write(str(count))
        url = 'https://pc.xuexi.cn/points/exam-paper-detail.html?id=' + str(count)

        browser.get(url)
        time.sleep(200)

def video():
    will_open = {}
    url = 'https://www.xuexi.cn/lgdata/2qfjjjrprmdh.json'
    response = requests.get(url,headers=headers,cookies=cookie)
    content = json.loads(response.text)

    for item in content:
        video_list.append(item['url'])

    while len(will_open.keys()) < 6:
        video_url = str(random.choice(video_list))
        video_id = video_url.split('=')[-1]
        check_length_url = 'https://boot-source.xuexi.cn/data/app/' + video_id + '.js'

        res = requests.get(check_length_url, headers=headers, cookies=cookie)
        will = re.findall('callback\((.*?)\)', res.text)[0]
        length_video = int(re.findall('\"play_length\":(\d+)', str(will))[0])
        if length_video >= 60 and length_video <= 120:
            will_open[video_url] = length_video

    # print(will_open)
    for url in will_open.keys():
        browser.get(url)
        time.sleep(int(will_open[url])+3)

def main():
    global cookies_list

    browser.get('https://pc.xuexi.cn/points/login.html?ref=https://pc.xuexi.cn/points/my-points.html')

    for i in range(2):
        browser.find_element_by_xpath('//*[@id="body-body"]').send_keys(Keys.PAGE_DOWN)
    time.sleep(3) #十秒钟扫码登陆时间
    cookies_list = browser.get_cookies()

    for item in cookies_list:
        cookie[item['name']] = item['value']
    print(cookies_list)
    print(cookie)

    get_all_task()

    video()
    reading()

    for item in obj:
        write(item)

if __name__ == '__main__':
    main()
