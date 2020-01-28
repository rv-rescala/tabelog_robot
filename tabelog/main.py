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
        
    for f in args.function:
        if f == "japan_ranking":
            output_path = f"{args.dump_path}/tabelog/japan_ranking_{get_today_date()}.json"
            print(f"output to {output_path}")
            result = JapanRankingSite(request).all_category_ranking()
            j = result.to_json(indent=4, ensure_ascii=False)
            with open(output_path, "w") as f:
                f.write(j)
    ## close        
    request.close()
    
if __name__ == "__main__":
    main()