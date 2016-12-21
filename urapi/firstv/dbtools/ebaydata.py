import MySQLdb
import json

def get_feedback_json(sellername):
    query = [
        "select *,",
        "concat(round(fstmonthpostive/(fstmonthpostive+fstmonthnegative)*100,2), '%') as score1,",
        "concat(round(sixmonthpostive/(sixmonthpostive+sixmonthnegative)*100,2), '%') as score6,",
        "concat(round(twemonthpostive/(twemonthpostive+twemonthnegative)*100,2), '%') as score12",
        "from firstv_feedback where sellername='%s' order by id desc limit 1" % sellername
    ]
    sql = " ".join(query)
    try:
        con = MySQLdb.connect(host='192.168.0.150', user='root', passwd='ur@2016!', db='urapi')
        cur = con.cursor(MySQLdb.cursors.DictCursor)
        con.set_character_set('utf8')
        cur.execute('set names utf8;')
        cur.execute('set character set utf8')
        cur.execute('set character_set_connection=utf8;')
        cur.execute(sql)
        row = cur.fetchone()
        row['createdDate'] = str(row['createdDate'])
        row['1VS6'] = round(float(row['score1'][:-1]) - float(row['score6'][:-1]),2)
        row['1VS12'] = round(float(row['score1'][:-1]) - float(row['score12'][:-1]), 2)
        row['6VS12'] = round(float(row['score6'][:-1]) - float(row['score12'][:-1]), 2)
        ret = json.dumps(row)
        return ret
    except Exception as e:
        error = json.dumps({"error":"no feedback data"})
        return error


if __name__ == '__main__':
    print get_feedback_json('sunshinegirl678')