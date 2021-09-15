import redis
import argparse
import sys

rdb = redis.Redis(host='127.0.0.1', port=6379, db=8, decode_responses=True)

parser = argparse.ArgumentParser(description='Find potential CPE names from a list of keyword')
parser.add_argument('--word', help='One or more keyword(s) to lookup', action='append')
args = parser.parse_args()

if args.word is None:
    print("Missing keyword(s)")
    parser.print_help()
    sys.exit(1)

k=[]
for keyword in args.word:
    k.append('w:{}'.format(keyword.lower()))

maxinter = len(k)
cpes = []
for x in reversed(range(maxinter)):
    ret = rdb.sinter(k[x])
    cpes.append(list(ret))


result = set(cpes[0]).intersection(*cpes)
print(result)

#for cpe in result:
#    rdb.zrank