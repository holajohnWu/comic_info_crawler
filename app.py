from flask import Flask, jsonify
from flask_cors import CORS
from comic_crawler import crawComicInfo
from datetime import datetime, timezone
import json
import os
from flask_apscheduler import APScheduler

newestRecordPath = './newest.json'
envPath = './env.json'

comicUrls = []
interval = 5
# load env
with open(envPath, 'r') as f:
    env = json.load(f)
    comicUrls = env['comics']
    interval = env['interval']
f.close()

app = Flask(__name__)
CORS(app)

# register scheduler
scheduler = APScheduler()


@scheduler.task('cron', id='scan_comic', hour='6')
def scanComic():
    print('start sanc_comic_scheduler')
    infos = crawComicInfo(comicUrls, interval)
    result = {'result': infos, 'modified': ''}
    with open(newestRecordPath, 'w') as f:
        state = os.stat(newestRecordPath)
        modified = datetime.fromtimestamp(state.st_mtime, tz=timezone.utc)
        result['modified'] = modified.isoformat()
        f.write(json.dumps(result))
    print('finish sanc_comic_scheduler')


scheduler.start()


@app.route('/', methods=['GET'])
def root():
    response = jsonify(message="Simple server is running")
    # Enable Access-Control-Allow-Origin
    return response


@app.route("/api/comic_info", methods=['PUT'])
def updateComicInfo():
    infos = crawComicInfo(comicUrls, interval)
    result = {'result': infos, 'modified': ''}

    with open(newestRecordPath, 'w') as f:
        state = os.stat(newestRecordPath)
        modified = datetime.fromtimestamp(state.st_mtime, tz=timezone.utc)
        result['modified'] = modified.isoformat()
        f.write(json.dumps(result))

    resp = jsonify(result)
    return resp


@app.route("/api/comic_info", methods=['GET'])
def getComicInfo():
    with open(newestRecordPath, 'r') as f:
        data = json.load(f)
        resp = jsonify(data)
    f.close()

    return resp


if __name__ == '__main__':
    app.run()
