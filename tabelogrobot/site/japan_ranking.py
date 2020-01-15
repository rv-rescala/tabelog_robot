import datetime
import sys
import requests
import re
import json
import time
from catscore.http.request import CatsRequest
from catscore.lib.logger import CatsLogging as logging
from catscore.lib.time import get_today_date, get_current_time
from bs4 import BeautifulSoup
from tabelogrobot.model.ranking import RankedItem
import itertools
import pandas as pd
from dataclasses import asdict
from tabelogrobot.site.detail import DetailSite

class JapanRankingSite:
    base_url = "https://tabelog.com"
    
    def __init__(self, request: CatsRequest):
        self.request = request

    def get_page(self, key=""):
        """[https://tabelog.com/key/rank/にアクセス]
        
        Returns:
            [type] -- [description]
        """
        if key == "":
            url = f"{self.base_url}/rank"
        else:
            url = f"{self.base_url}/{key}/rank"
        logging.info(f"request to {url}")
        response = self.request.get(url=url, response_content_type="html")
        return response

    def category_ranking(self, keyword, url):
        """[指定されたurlのランク付きアイテムを取得]
        
        Arguments:
            folder {[type]} -- []
        
        Returns:
            [type] -- [description]
        """
        def _parse_li(li):
            shop_name = li.find("a", {"class": "list-rst__rst-name-target"}).text
            shop_link = li.find("a", {"class": "list-rst__rst-name-target"}).get("href")
            shop_target = li.find("span", {"class": "list-rst__area-genre"}).text
            shop_photo = li.find("p", {"class": "list-rst__photo-item"}).find("img").get("src")
            shop_start = li.find("span", {"class": "c-rating__val c-rating__val--strong"}).text
            shop_review_count = li.find("a", {"class": "list-rst__rvw-count-target"}).text.split("件")[0]
            shop_review_link = li.find("a", {"class": "list-rst__rvw-count-target"}).get("href")
            shop_budget = li.findAll("span", {"class": "cpy-dinner-budget-val"})
            shop_diner_budget = shop_budget[0].text
            shop_lunch_budget = shop_budget[1].text
            detail: DetailSite = DetailSite(self.request, shop_link)
            shop_pr_comment = detail.pr_comment
            shop_pr_comment_title = shop_pr_comment["pr_comment_title"]
            shop_pr_comment_first = shop_pr_comment["pr_comment_first"]
            # list-rst__comment-item
            shop_comments = ",".join(list(map(lambda x: x.find("strong").text, li.findAll("li", {"class": "list-rst__comment-item"}))))
            return RankedItem(shop_name=shop_name,
                              shop_link=shop_link,
                              shop_target=shop_target,
                              shop_photo=shop_photo,
                              shop_start=shop_start,
                              shop_review_count=shop_review_count,
                              shop_review_link=shop_review_link,
                              shop_diner_budget=shop_diner_budget,
                              shop_lunch_budget=shop_lunch_budget,
                              shop_comments=shop_comments,
                              shop_pr_comment_title=shop_pr_comment_title,
                              shop_pr_comment_first=shop_pr_comment_first)
        
        soup = self.request.get(url=url, response_content_type="html").content
        rank_name = soup.find("strong", "list-condition__title").text.replace("\n","").replace(" ","")
        item_li = soup.find("div", {"class", "top20-ranking"}).find("ul").findAll("li", {"class", "list-rst--rank20"})
        items = list(map(lambda i: _parse_li(i), item_li))
        return items

    @property
    def category_ranking_menu(self):
        """[ランキング一覧(カテゴリ別)を取得]
        
        Returns:
            [type] -- [description]
        """
        li = self.get_page().content.find("ul", {"class", "rank-level2"}).findAll("li", {"class", "level2"})
        result = list(map(lambda i: (i.text.replace("\n",""), i.find("a").get("href")), li))
        result.append(("総合",f"{self.base_url}/rank"))
        logging.info(result)
        return result
    
    def all_category_ranking(self, pandas=False):
        """[summary]
        """
        menu = self.category_ranking_menu
        r = list(map(lambda m: self.category_ranking(m[0], m[1]), menu))
        result = list(itertools.chain.from_iterable(r))
        if pandas:
            return pd.DataFrame([asdict(x) for x in result])
        else:
            return result