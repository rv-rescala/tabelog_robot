from __future__ import print_function

import argparse
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark import SparkContext
from tabelog.model.ranking import RankedItemTable, CookedRankedItemTable
from catscore.db.mysql import MySQLConf
from catscore.word.mecab import CatsMeCab

def main():
    # spark
    conf = SparkConf()
    conf.setAppName('tabelog')
    sc: SparkContext = SparkContext(conf=conf)
    spark:SparkSession = SparkSession(sc)

    # init
    parser = argparse.ArgumentParser(description='pyspark app args')
    parser.add_argument('-ip', '--input_path', type=str, required=True, help='input folder path')
    parser.add_argument('-db', '--db_conf', type=str, required=True, help='input db conf path')
    parser.add_argument('-md', '--mecab_dict', type=str, help='input mecab dict path')
    args = parser.parse_args()
    print("todb_job: start")
    print(f"args: {args}")
    mysql_conf = MySQLConf.from_json(args.db_conf)
    print(f"mysql_conf {mysql_conf}")
    
    # convert
    # step1
    ranked_item_df = RankedItemTable.from_file_as_df(spark, args.input_path)
    RankedItemTable.to_db(spark=spark, df=ranked_item_df, mysql_conf=mysql_conf)
    # step2
    cooked_ranked_item = RankedItemTable.cooking(spark=spark, df=ranked_item_df, mecab_dict=args.mecab_dict)
    CookedRankedItemTable.to_db(spark=spark, df=cooked_ranked_item, mysql_conf=mysql_conf)
    
if __name__ == '__main__':
    main()