from rq import Queue
from redis import Redis
from flask import Flask

import time
import json

from worker_processes import get_new_ads
from avito import get_entry

redis_conn = Redis()
q = Queue(connection=redis_conn)
app = Flask(__name__)

@app.route('/process')
def process():
    job = q.enqueue(get_new_ads, 'https://www.avito.ru/moskva?q=ps4')
    time.sleep(2)
    return job.id
  
@app.route('/result/<id>')
def result(id):
    try:
        job = q.fetch_job(id)
        if job.is_finished:
            return json.dumps({"words_counted": job.result}, ensure_ascii=False)
        else:
            return "not ready", 202
    except:
        return "not found", 404

if __name__ == "__main__":
    app.run('127.0.0.1')
    while True:
        time.sleep(1)
        job = q.enqueue(get_entry, 'https://www.avito.ru/moskva?q=ps4')
