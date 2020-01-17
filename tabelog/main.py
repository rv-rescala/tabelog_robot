import argparse
import logging
from tabelog.site.japan_ranking import JapanRankingSite
from tabelog.model.ranking import CookedRankedItemTable
from tabelog.site.detail import DetailSite
from catscore.http.request import CatsRequest
from catscore.lib.time import get_today_date
from sqlalchemy import create_engine
from catscore.db.mysql import MySQLConf

def main():
    parser = argparse.ArgumentParser(description="tabelog robot")

    # args params
    parser.add_argument('-f', '--function', nargs='*', choices=['japan_ranking', 'detail', 'cache'], help="functions")
    parser.add_argument('-d', '--dump_path', help="result dump path")
    parser.add_argument('-db', '--db_conf', type=str, help='input db conf path')
    args = parser.parse_args()
    print(args)
    # init
    request: CatsRequest = CatsRequest()
    engine = None
    if args.db_conf != None:
        mysql_conf = MySQLConf.from_json(args.db_conf)
        print(f"mysql_conf {mysql_conf}")
        engine = create_engine(mysql_conf.connection_uri("pymysql"), encoding="utf-8", echo=False)
    if args.dump_path == None:
        dump_path = "/tmp"
    else:
        dump_path = args.dump_path
        
    for f in args.function:
        if f == "japan_ranking":
            output_path = f"{dump_path}/tabelog/japan_ranking_{get_today_date()}.csv"
            print(f"output to {output_path}")
            result = JapanRankingSite(request).all_category_ranking(pandas=True)
            result.to_csv(output_path)
        elif f == "detail":
            result = DetailSite(request, "https://tabelog.com/aichi/A2301/A230104/23050337/")
        elif f == "cache":
            output_path = f"{dump_path}/tabelog/japan_ranking_{get_today_date()}.json"
            print(f"output to {output_path}")
    
    ## close        
    request.close()
    
if __name__ == "__main__":
    main()