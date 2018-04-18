import requests 
import time
import datetime
import calendar
import pytz
import sys
import re
import argparse # try getopt next time

def request_time(target_url, tz='Asia/Taipei'):
    """ Estimate server time by local timestamps
    Args:
        target_url: The url of target server.
    Return:
        offset: The possible offset between local time and server time.
    """
    if target_url == None:
        raise Exception('Check the input of request_time')
    
    if not url_validation(target_url):
        raise Exception('Make sure the url is valid')

    t0 = time.time()
    req = requests.get(target_url)
    t3 = time.time()
    duration = t3 - t0
    req_t = req.headers['Date']

    # change GMT to GMT+8, turn it into unix timestamp
    dt_local = pytz.timezone(tz).localize(datetime.datetime.strptime(req_t, "%a, %d %b %Y %H:%M:%S GMT"))
    t1p = calendar.timegm(dt_local.timetuple())
    # t1p = time.mktime(datetime.datetime.strptime(req_t, "%a, %d %b %Y %H:%M:%S GMT").timetuple())

    # offset to estimate server time
    offset = t1p - (t0 + duration / 2.0)
    return offset

def url_validation(url):
    """ ref:https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    Use django url validation regex
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def update_output(offset, min):
    """ Update server time every 30 ms
    """
    iters = int(min * 60 * 1000 / 30)
    start_t = time.time()
    print('--- Start Tracing Server Time for {} mins ---'.format(min), end='\n', flush=True)
    while iters:
        current_t = time.time()
        if current_t - start_t < 0.03:
            continue
        else:
            server_ft = datetime.datetime.fromtimestamp(time.time() + offset).strftime('%d/%m/%Y %H:%M:%S.%f')
            print("Server Time: " + server_ft, end="\r", flush=True)
            iters -= 1
            start_t = time.time()
    print(flush=True)
    print('--- End of tracking server time ---', end="\n")


def main():
    # setup args
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="enter the url of target server")
    parser.add_argument("-d", "--duration", help="track the server time for a duration in minutes",
                        type=int, default=5)
    args = parser.parse_args()

    # request tixCraft ticket system
    # target_url = 'https://tixcraft.com/'
    # target_url = 'https://www.wikipedia.org/'

    offset = request_time(args.url)
    update_output(offset, args.duration)

if __name__ == '__main__':
    main()