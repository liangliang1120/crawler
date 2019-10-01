
"""
Created on Sun Sep 15 14:29:11 2019

@author: us
"""

import io

import sys

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

from bs4 import BeautifulSoup as bs
import requests
import json

START_URL = "https://movie.douban.com/subject/25779217/comments"
HEADERS = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Referer':'https://www.douban.com/accounts/login?source=movie',
'Cookie':'bid=RD-3z-EM9-U; ap_v=0,6.0; _pk_ses.100001.4cf6=*; __utma=30149280.1286780158.1568533810.1568533810.1568533810.1; __utmc=30149280; __utmz=30149280.1568533810.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; dbcl2="170719751:yMNkbSQ0GIU"; ck=EzrC; _pk_id.100001.4cf6=9c22c3b036952374.1568533809.1.1568533847.1568533809.; __utmt_douban=1; __utmb=30149280.2.10.1568533810; __utma=223695111.1817256674.1568533847.1568533847.1568533847.1; __utmb=223695111.0.10.1568533847; __utmc=223695111; __utmz=223695111.1568533847.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; push_noty_num=0; push_doumail_num=0',
'Connection':'keep-alive Cache-Control: max-age=0'
}




def find_next(dom):
    next_button = dom.find('a', {'class': 'next'})
    if next_button:
        href = next_button.attrs['href']
        return START_URL + href
    else:
        return

def parse_comment(comment):
    cid = comment.attrs['data-cid']
    vote = comment.find('span', {'class': 'votes'}).text
    star = comment.find('span', {'class': 'rating'})
    star = star.attrs['title'] if star else "未评分"
    content = comment.find('p').text
    return {
        "comment": content,
        "vote": vote,
        "star": star,
        "cid": cid
    }

def parse_comments(dom):
    comments = dom.find_all('div', {'class': 'comment-item'})
    return [parse_comment(comment) for comment in comments]


def crawler(url, n=0):
    req = requests.get(url, headers=HEADERS)
    # req.encoding = 'utf8'
    print("Crawling {}".format(url))
    if req.status_code == 200:
        dom = bs(req.text, 'lxml')
        next_button = find_next(dom)
        comments = parse_comments(dom)
        with open("result/comment_{}.json".format(n), 'w') as fp:
            try:
                fp.write(json.dumps(comments, ensure_ascii=False, indent=4))
            except:
                pass
        n = n + 1
        if next_button:
            crawler(next_button, n)
    else:
        print("Fail")

if __name__ == "__main__":
    print(crawler(START_URL))