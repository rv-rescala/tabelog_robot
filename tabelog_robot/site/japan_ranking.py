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
from kakaku_robot.model.item import RankedItem
import itertools
import pandas as pd
from dataclasses import asdict

class JapanRanking:
    base_url = "https://tabelog.com"
    
    def __init__(self, proxy=None):
        """[summary]
        
        Arguments:
            headless {[type]} -- [description]
        
        Keyword Arguments:
            proxy {[type]} -- [description] (default: {None})
        """
        self.proxy = proxy
        self.request = CatsRequest()
        
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
            return {"shop_name": shop_name, "shop_link": shop_link, "shop_target": shop_target}
        
        soup = self.request.get(url=url, response_content_type="html").content
        rank_name = soup.find("strong", "list-condition__title").text.replace("\n","").replace(" ","")
        item_li = soup.find("div", {"class", "top20-ranking"}).find("ul").findAll("li", {"class", "list-rst--rank20"})
        items = list(map(lambda i: _parse_li(i), item_li))
        print(items)

    @property
    def category_ranking_menu(self):
        """[ランキング一覧(カテゴリ別)を取得]
        
        Returns:
            [type] -- [description]
        """
        li = self.get_page().content.find("ul", {"class", "rank-level2"}).findAll("li", {"class", "level2"})
        result = list(map(lambda i: (i.text.replace("\n",""), i.find("a").get("href")), li))
        result.append(("総合",f"{self.base_url}/rank")).find("ul")
        logging.info(result)
        return result