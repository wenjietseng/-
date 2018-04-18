# Web Server Clock
嘗試靠偵測遠端網站時間還準確按下購票

## Content:
- Get server time and estimate it by local time (done)
- A parser can click the "buy ticket" and go through identifier (not finished)

## Usage:
`$ python3 estimate_server_time.py "target_url" -d minutes_to_track`

## Requirements:
Python (3.6.5), requests (2.18.4)

## License:
MIT

## References:
- [網路搶票小幫手](http://columns.chicken-house.net/2017/01/05/webserverclock-release/#release-notes)
- [Python 時區轉換](https://kkc.github.io/2015/07/08/dealing-with-datetime-and-timezone-in-python)