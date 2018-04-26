from bs4 import BeautifulSoup
import requests
import time
import random
import re

url = "https://yande.re/pool?page=30"
head = {}
head['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"

for i in range(10):
    a = 0
    i += 1
    soup1 = BeautifulSoup(requests.get(url,headers=head).text, features='lxml')
    firstimg_url = soup1.find_all('tr',{"class":("even","odd")})
    url = 'https://yande.re' + soup1.find('div',{'id':'paginator'}).find('a',{'rel':'next'})['href']
    print('Start')
    for url_r in firstimg_url:
       time.sleep(round(random.uniform(0,1),2))
       secondimg_url = BeautifulSoup(requests.get('https://yande.re' + url_r.find('a')['href'],headers=head).text, features='lxml').find_all('ul',{'id':'post-list-posts'})
       for url2 in secondimg_url:
           r1 = url2.find_all('a',{'class':'thumb'})
       a += 1
       if r1 == [] or len(r1) >100:
           continue
       for url_r3 in r1:
           r2 = 'https://yande.re' + url_r3['href']
           time.sleep(round(random.uniform(1,2),2))
           soup3 = BeautifulSoup(requests.get(r2,headers=head).text, features='lxml')
           score = soup3.find('span',{'id':re.compile('post-score.+')})
           if i < 3 :
              if int(score.get_text()) < 120:
                 continue
           elif int(score.get_text()) < 130:
              continue
           select_img = soup3.find('div',{'class':'sidebar'})
           url3 = select_img.find('a',{'class':'original-file-unchanged'})
           if url3 == None:
              url3 = select_img.find('a',{'class':'original-file-changed'})
              if url3 ==None:
                  continue
           time.sleep(round(random.uniform(0,1),2))
           r = requests.get(url3['href'], stream=True)
           image_name = url3['href'].split('/')[-1]
           with open(r'C:\Users\Saber\Desktop\爬虫\%s' %image_name, 'wb') as f:
               for chunk in r.iter_content(chunk_size=128):
                   f.write(chunk)
               print('%s\n页数 : %d , 第 %d tags\n' %(image_name,i,a))