from dataclasses import dataclass, field
from pyspark.sql import SparkSession, DataFrame
from catscore.db.mysql import MySQLConf
from catscore.word.mecab import CatsMeCab

class RankedItemTable:
    _table_name = "tableog_ranked_item"
    
    @classmethod
    def from_file_as_df(cls, spark:SparkSession, input_path:str):
        """
        """
        input_path = f"{input_path}/*.csv"
        print(f"RankedItemTable: input path is {input_path}")
        df = spark.read.option("header", "true").csv(input_path).drop("_c0")
        return df
    
    @classmethod
    def to_db(cls, spark:SparkSession, df:DataFrame, url:MySQLConf):
        df.write.jdbc(mysql_conf.connection_uri("jdbc"), table=cls._table_name, mode='overwrite')
    
    @classmethod
    def cooking(cls, spark:SparkSession, df:DataFrame, mecab_dict: str):
        def _cooking(d):
            s = f'{d["shop_comments"]},{d["shop_pr_comment_title"]},{d["shop_pr_comment_first"]}'
            mecab = CatsMeCab(mecab_dict)
            parsed_s = mecab.parse(str(s))
            noun_s = list(filter(lambda r: r.word_type == "名詞", parsed_s))
            noun_one_str = list(map(lambda r: f"{r.word}", noun_s))
            nouns = ",".join(noun_one_str)
            result = CookedRankedItem(
                rank_keyword = d["rank_keyword"],
                rank_num = d["rank_num"],
                shop_name = d["shop_name"],
                shop_link = d["shop_link"],
                shop_target = d["shop_target"],
                shop_photo = d["shop_photo"],
                shop_start = d["shop_start"],
                shop_review_count = d["shop_review_count"],
                shop_review_link = d["shop_review_link"],
                shop_diner_budget = d["shop_diner_budget"],
                shop_lunch_budget = d["shop_lunch_budget"],
                shop_comments = d["shop_comments"],
                shop_pr_comment_title = d["shop_pr_comment_title"],
                shop_pr_comment_first = d["shop_pr_comment_first"],
                update_date = d["update_date"],
                nouns = nouns)
            return result
        return df.rdd.map(lambda d: _cooking(d)).toDF()
    
@dataclass(frozen=True)
class RankedItem:
    rank_keyword: str
    rank_num: str
    shop_name: str
    shop_link: str
    shop_target: str
    shop_photo: str
    shop_start: str
    shop_review_count: str
    shop_review_link: str
    shop_diner_budget: str
    shop_lunch_budget: str
    shop_comments: str
    shop_pr_comment_title: str
    shop_pr_comment_first: str
    update_date: str
    
class CookedRankedItemTable:
    _table_name = "cooked_tableog_ranked_item"
    
    @classmethod
    def to_db(cls, spark:SparkSession, df:DataFrame, mysql_conf:MySQLConf):
        df.write.jdbc(mysql_conf.connection_uri("jdbc"), table=cls._table_name, mode='overwrite')
    
    @classmethod
    def from_db_as_dataframe(cls, engine):
        pass
        
    

@dataclass(frozen=True)
class CookedRankedItem:
    rank_keyword: str
    rank_num: str
    shop_name: str
    shop_link: str
    shop_target: str
    shop_photo: str
    shop_start: str
    shop_review_count: str
    shop_review_link: str
    shop_diner_budget: str
    shop_lunch_budget: str
    shop_comments: str
    shop_pr_comment_title: str
    shop_pr_comment_first: str
    update_date: str
    nouns: str
