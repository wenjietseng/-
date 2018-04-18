import requests 
import time
import datetime
import calendar
import pytz
# request tixCraft ticket system
target_url = 'https://tixcraft.com/'
# target_url = 'https://api.github.com/events'

t0 = time.time()
req = requests.get(target_url)
t3 = time.time()
duration = t3 - t0

req_t = req.headers['Date']
# print(req.headers)
# change GMT to GMT+8, turn it into unix timestamp
dt_local = pytz.timezone('Asia/Taipei').localize(datetime.datetime.strptime(req_t, "%a, %d %b %Y %H:%M:%S GMT"))
t1p = calendar.timegm(dt_local.timetuple())
# t1p = time.mktime(datetime.datetime.strptime(req_t, "%a, %d %b %Y %H:%M:%S GMT").timetuple())
# print("local\tt0:\t" + str(t0))
# print("server\tt1p:\t" + str(t1p))
# print("local\tt3:\t" + str(t3))

# offset to estimate server time
offset = t1p - (t0 + duration / 2.0)
server_t = (time.time() + offset)
server_ft = datetime.datetime.fromtimestamp(server_t).strftime('%d/%m/%Y %H:%M:%S')
print("Server Time:\t " + server_ft)




