import argparse
import logging
from tabelogrobot.site.japan_ranking import JapanRankingSite
from tabelogrobot.site.detail import DetailSite
from catscore.http.request import CatsRequest

def main():
    parser = argparse.ArgumentParser(description="tabelog robot")

    # args params
    parser.add_argument('-f', '--function', nargs='*', choices=['japan_ranking', 'detail'], help="functions")
    parser.add_argument('-d', '--dump_path', help="result dump path", required=True)
    args = parser.parse_args()
    print(args)
    
    request: CatsRequest = CatsRequest()
    for f in args.function:
        if f == "japan_ranking":
            output_path = f"{args.dump_path}/japan_ranking.csv"
            result = JapanRankingSite(request).all_category_ranking(pandas=True)
            result.to_csv(output_path)
        elif f == "detail":
            result = DetailSite(request, "https://tabelog.com/aichi/A2301/A230104/23050337/")
    request.close()
if __name__ == "__main__":
    main()