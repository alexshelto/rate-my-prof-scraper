

import argparse

from RMP import RMP

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='school id is needed to scrape scores')

    args = parser.parse_args()
    score_file = open('scores.json', 'w')

    rmp = RMP(args.id)
    obj = rmp.scrape_scores()

    json.dump(obj, score_file)
    score_file.close()

    return 0

# Code to seed data base: can take out "send_to_kv()" and save to dict if neccesary
if __name__ == '__main__':
    exit(main())
