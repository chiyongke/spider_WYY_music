from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
import time
import re 
import requests
import datetime
#selenium渲染提取歌曲名称和资源url
def selencolor():
	songname=[] #存放歌曲名
	songurl=[]  #存放歌曲资源url
	songername=[]  #存放歌手名

	driver=webdriver.Chrome(executable_path=r'D:\谷歌浏览器\chromedriver.exe')
	driver.implicitly_wait(20)#隐性等待
	driver.get('https://music.163.com/#/discover/toplist')#发送请求，
	time.sleep(5) #等待加载页面信息
	driver.switch_to.frame(driver.find_element_by_css_selector("iframe.g-iframe")) 	#iframe框架解析
	#data=driver.page_source 把渲染的网页信息爬取下来
	urls=driver.find_elements_by_css_selector('div.ttc')
	names=driver.find_elements_by_css_selector('div.text')
	for i in names:
		songername.append(i.get_attribute('title'))  #获取存放歌手名称
	#查找歌曲名称和资源
	for i in urls:
		link=i.find_element_by_tag_name('a').get_attribute('href') #获取每一首歌的url
		ID=re.search(r'id=\d+',link).group()#获取每一首歌资源的url
		name=i.find_element_by_tag_name('b').get_attribute('title')	#获取歌名
		#保存歌名和歌曲资源url
		songurl.append(r'http://music.163.com/song/media/outer/url?'+ID)  #http://music.163.com/song/media/outer/url?外链链接
		songname.append(name)
	print("已经提取歌曲名称和歌曲资源url完毕。。。。现退出selenium")
	driver.quit()
	download(songname,songurl,songername)
#下载歌曲并保存歌曲
def download(songname,songurl,songername):
	k=0
	global h
	h=0
	headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400'}
	for i  in songurl:
		#try防止有些歌曲爬取失败而停止运行
		try:
			print('准备下载%s'%(songname[k])+'   '+'演唱者：%s'%(songername[k]))
			songdata=requests.get(i,headers=headers).content
			with open(r'F:\downicloudlmusic\{}.mp3'.format(songname[k]+'---%s'%(songername[k])),'wb') as f:
				f.write(songdata)
			print('已下载完毕!!!')
			h+=1
		except Exception as e:
			print('%s下载失败'%(songname[k]))
		finally:
			k+=1
			time.sleep(0.2) 
if __name__ == '__main__':
	print('现在时间是：',datetime.datetime.now())
	print('即将爬取网易云排行榜歌曲。。。。')
	selencolor()
	print('已成功爬取%d首歌'%h)
	print('现在时间是：',datetime.datetime.now())