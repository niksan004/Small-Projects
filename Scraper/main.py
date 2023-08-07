import mysql.connector
import json
import time

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'
]


def create_mysql_cursor():
    conn_mysql = mysql.connector.connect(user=user,
                                         password=password,
                                         host=host,
                                         database=database)
    cur_mysql = conn_mysql.cursor()

    return conn_mysql, cur_mysql


def insert_into_database(data, cur):
    query = 'INSERT INTO inmarsat (imo, service, number) VALUES '

    values = ''
    cnt = 0
    for rec in data:
        if cnt > 0:
            values += ', '
        values += str(rec)
        cnt += 1

    query += values
    query += ' ON DUPLICATE KEY UPDATE service = VALUES(service), number = VALUES(number), tstamp = NOW()'
    cur.execute(query)


def get_inmarsat(imo, proxy):
    url = url + str(imo)

    headers = {'User-Agent': USER_AGENTS[int(time.time()) % len(USER_AGENTS)]}
    proxy = {'http': proxy}

    try:
        res = requests.get(url, headers=headers, proxies=proxy, timeout=10)
    except requests.exceptions.ConnectionError:
        # print('connection error')
        return
    except requests.exceptions.ReadTimeout:
        # print('read timeout error')
        return

    if res.status_code != 200:
        # print('status != 200')
        return

    if res.headers['Content-Type'] != 'application/json;charset=utf-8':
        # print('file not json')
        return

    if len(res.content) <= 0:
        # print('empty file')
        return

    json_file = json.loads(res.content)

    data = []
    for sample in json_file['vessels'][0]['inmarsatNumbers']:
        data.append((imo, sample['service'], sample['number']))

    if len(data) > 0:
        conn, cur = create_mysql_cursor()

        delete_old(imo, cur)
        insert_into_database(data, cur)

        conn.commit()
        cur.close()
        conn.close()
