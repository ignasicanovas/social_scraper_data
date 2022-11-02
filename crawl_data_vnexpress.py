# from ast import main
from turtle import title
from newspaper import Article
from bs4 import BeautifulSoup
import urllib.request
import re
import csv
import newspaper

def get_page_news_feeds(number=21):
    link_page_news_feeds = []
    for num in range(1,number):
        url =  'https://vnexpress.net/kinh-doanh/chung-khoan'
        url += "-p"+str(num)
        link_page_news_feeds.append(url)

    return link_page_news_feeds

# tìm tất cả link
def get_urls_new_feeds(url):

    # url =  'https://vnexpress.net/kinh-doanh/chung-khoan'
    link_new_feeds = []
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    new_feeds = soup.find(
        'div', class_='col-left col-left-new col-left-subfolder').find_all('a', class_="thumb thumb-5x3") 

    for feed in new_feeds:
        # title = feed.get('title')
        link = feed.get('href')
        link_new_feeds.append(link)
        # print(link)
        # print('Title: {} - Link: {}'.format(title, link))

    # cnn_paper = newspaper.build(url)

    # article = Article(url)
    # article.download()
    # article.parse()

    # for article in cnn_paper.articles:
    #     link = article.url
    #     link_new_feeds.append(link)

    # print(link_new_feeds)
    return link_new_feeds

def get_content_all_new_feeds(urls):

        for url in urls:
            article = Article(url)
            article.download()
            article.parse()
            
            titl = article.title
            content = re.sub('\\n+','', article.text)

            # lay thoi gian publish date 
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            find_date = soup.find('span', class_='date')

            if find_date != None:
                date = re.split(r",", find_date.text)[1].strip()

            # luu ket qua lai thanh file csv
            with open('data.txt', 'w') as f:
                writer = f.writer([titl, content, date])
            # f.write(','.join([titl, content, date]))
            # f.write('\n')
            print('Done!!!!')

if __name__ == '__main__':

    with open('data.csv', 'w', encoding = 'utf-8') as f:
        urls_page = get_page_news_feeds()
        # print(urls_page)
        writer = csv.writer(f)
        writer.writerow(['Title', 'Content', 'date'])

        for url in urls_page:
            urls = get_urls_new_feeds(url)
            get_content_all_new_feeds(urls)




    # lỗi ở page p14 - ngày 6/1/2022 
    # url = 'https://vnexpress.net/quy-dau-tu-phan-lan-lien-tuc-chot-loi-ceo-4411526.html'
    # with open('data.csv', 'a', encoding="utf-8") as csv_file:
    #     writer = csv.writer(csv_file)

    #     article = Article(url)
    #     article.download()
    #     article.parse()
        
    #     titl = article.title
    #     content = re.sub('\\n+','', article.text)

    #     # lay thoi gian publish date 
    #     page = urllib.request.urlopen(url)
    #     soup = BeautifulSoup(page, 'html.parser')
    #     find_date = soup.find('span', class_='date')

    #     if find_date != None:
    #         date = re.split(r",", find_date.text)[1].strip()

    #     # luu ket qua lai thanh file csv
    #         writer.writerow([titl, content, date])
    #         print('Done!!!!')