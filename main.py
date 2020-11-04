import requests 
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
import argparse
from threading import RLock

lock = RLock()

def get_line(file):
    with open(file) as input_file:
        for line in input_file:
            yield line.strip()

def make_request(url):
    if url.strip() != "":
        soup = BeautifulSoup(requests.get('https://www.mustat.com/' + url.replace('http://','').replace('https://','')).text,'html5lib')
        print(url.replace('http://','').replace('https://',''))
        with open('result.txt', 'a') as f:
            try:
                f.write(url.replace('http://','').replace('https://','') + ' ; ' + soup.select_one('span.underline:nth-child(1)').text + '\n')
            except:
                print('404')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--pool", help="20", type=str)
    parser.add_argument("-f","--file", help="url.txt", type=str)
    args = parser.parse_args()

    if args.file is not None and args.pool is not None:
        input_file = args.file
        try:
            pool_size = int(args.pool)
        except ValueError:
            exit('Pool size value must be int')
        pool = Pool(pool_size)
        pool.map(make_request, get_line(input_file))
