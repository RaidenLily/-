from bs4 import BeautifulSoup
import requests
import random
import re
import multiprocessing as mp

url = "https://konachan.com/post/popular_by_week"
head = {}
head['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
unseen = []

def first_crawl():
    global text1,unseen
    print('Start')
    soup1 = BeautifulSoup(requests.get(url,headers=head).text, features='lxml')
    firstimg_url = soup1.find('ul',{"id":'post-list-posts'})
    haha = firstimg_url.find_all('img')
    text1 = soup1.find('div',{'id':'post-popular'}).find('h3').get_text()
    t = firstimg_url.find_all('a',{'class':'thumb'})
    for p in t:
        unseen = unseen + [p['href']]

def crawl_parse(a_url):
    soup2 = BeautifulSoup(requests.get('http://konachan.com'+a_url,headers=head).text, features='lxml')
    select_img = soup2.find('div',{'class':'sidebar'})
    url3 = select_img.find('a',{'class':'original-file-unchanged'})
    if url3 == None:
        url3 = select_img.find('a',{'class':'original-file-changed'})
        if url3 == None:
            url3 = select_img.find('a',{'class':'original-file-changed highres-show'})
    r = requests.get(url3['href'], stream=True)
    image_name = url3['href'].split('/')[-1]
    with open(r'C:\Users\Saber\Desktop\k站周榜\%s' %image_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)
        print(image_name)

if __name__== '__main__':
        p = mp.Pool(30)
        first_crawl()
        for a_url in unseen:
            p.apply_async(crawl_parse,args=(a_url,))
        p.close()
        p.join()
        unseen.clear()
        print('\n\n%s' %text1)