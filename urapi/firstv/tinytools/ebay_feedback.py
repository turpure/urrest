import requests
from bs4 import BeautifulSoup
from gevent import monkey; monkey.patch_socket()
import gevent
import logging
import MySQLdb
import datetime
#logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logger.addHandler(console)

create_datetime = datetime.datetime.now()


def get_sellerid():

    con = MySQLdb.connect(host='192.168.0.150', user='root', passwd='ur@2016!', db='urapi')
    cur = con.cursor(MySQLdb.cursors.DictCursor)
    sql = 'select sellerName from firstv_ebayaccount '

    try:
        cur.execute(sql)
        for row in cur.fetchall():
            print row['sellerName']
            yield row['sellerName']
    except Exception as e:
    	logger.error(e)
    finally:
        cur.close()
        con.close()

def insert_data(sellerid, data, create_datetime):
    con = MySQLdb.connect(host='192.168.0.150', user='root', passwd='ur@2016!', db='urapi')
    cur = con.cursor()
    query = ['insert into firstv_feedback (sellerName,isTopRated,fstmonthPostive,fstmonthNetural,fstMonthNegative,sixMonthPostive,sixMonthNetural,',
    	'sixMonthNegative,tweMonthPostive,tweMonthNetural,tweMonthNegative,createdDate)',
    	'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ']
    sql = ''.join(query)
    try:
        cur.execute(sql, (sellerid, data[0], data[1], data[4], data[7], data[2],data[5], data[8], data[3],data[6],data[9],create_datetime))
        con.commit()
        # print "%s:inserting feedback for %s" % (str(datetime.datetime.now()), sellerid)
        logger.info('Inserting feddback data for %s' % sellerid)
    except Exception as e:
        logger.warn(e)
    con.close()

def fetch_feedback(sellerid):
    base_url = [
        'http://feedback.ebay.com/ws/eBayISAPI.dll?ViewFeedback2&userid=',
        sellerid
    ]
    data = []
    url = ''.join(base_url)

    logger.info('Start to fetch %s' % sellerid)

    for i in range(10):
        try:
            r = requests.get(url)
            break
        except:
            r = None
    if r:
    	try:
	        body = r.content
	        soup = BeautifulSoup(body, 'lxml')
	        is_top_rated = soup.find(text='Top-rated seller')
	        data.append(is_top_rated)
	        feedback_trs = soup.find_all('tr', {'class':'fbsSmallYukon'})
	        for tr in feedback_trs:
	            feedback_tds = tr.find_all('td',{'id': 'RFRId'})
	            for td in feedback_tds:
	                 data.append(td.text)
	except Exception as e:
		logger.warn(e)
	# return datad
	logger.debug(data)
	insert_data(sellerid,data,create_datetime)
    else:
    	logger.error('no fetching data from %s' % sellerid)

def get_feedback():
    jobs = [gevent.spawn(fetch_feedback, serller) for serller in get_sellerid()]
    gevent.wait(jobs)
if __name__ == '__main__':
    main()
     
   





        

	




