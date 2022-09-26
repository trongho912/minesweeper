from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np
from math import sqrt
import datetime
import os, time
# /html/body/div[3]/div[2]/div[2]/form/div[3]/div[1]/div/table/tbody/tr/td/div/div/div[1]/div/div

def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr   = arr[size:]
    arrs.append(arr)
    return arrs

def getboard(url):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    url_file_drive = os.path.join('etc','chromedriver.exe')
    driver = webdriver.Chrome(executable_path=url_file_drive, chrome_options=chrome_options)
    driver.get(url)
    target = driver.find_elements("class name",'number')
    # for data in target:
    #     block = data.find_element("class name","number")
    # for i in block:
    rs=[]
    target.pop(0)
    for data in target:
        if data.text!='':
            rs.append(int(data.text))
        else:
            rs.append('w')
    arr=np.reshape(rs,(int(sqrt(len(rs))),int(sqrt(len(rs)))))
    # print (type())
    arr=split(rs,int(sqrt(len(rs))))
    # time.sleep(4)
    driver.close()
    return arr
