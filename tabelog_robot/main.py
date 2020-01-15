import argparse
import logging
from tabelog_robot.site.japan_ranking import JapanRanking

def main():
    parser = argparse.ArgumentParser(description="tabelog robot")

    # args params
    parser.add_argument('-f', '--function', nargs='*', choices=['japan_ranking'], help="functions")
    #parser.add_argument('-d', '--dump_path', help="result dump path", required=True)
    args = parser.parse_args()
    print(args)
    
    for f in args.function:
        if f == "japan_ranking":
            result = JapanRanking().category_ranking('和食', 'https://tabelog.com/washoku/rank/')
            
            
if __name__ == "__main__":
    main()