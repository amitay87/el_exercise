import hashlib
import multiprocessing

from sanic import Sanic
from sanic.response import json
import grequests

from db import DBManager
import second_service
import json as python_json


app = Sanic("handle notify app")


def file_as_bytes(file):
    with file:
        return file.read()


@app.route('/notify_record_completion', methods=['POST'])
async def handle_notify_record_completion(request): # TODO: refactor function name
    body_json = python_json.loads(request.body.decode('ascii').replace('\'', '\"'))
    try:
        recording_files = body_json['payload']['object']['recording_files']
    except KeyError:
        return json({'status': 'recording files was not found'})
    urls = [rf['download_url'] for rf in recording_files]
    rs = (grequests.get(u) for u in urls)
    downloads = grequests.map(rs)

    for idx, file in enumerate(recording_files):
        extension = file['file_extension']
        id = file['id']
        saved_filename = f"{id}.{extension}"

        with open(saved_filename, 'wb') as f:
            f.write(downloads[idx].content)

        # TODO: consider calculating hash asyncronously
        calculated_hash = hashlib.md5(file_as_bytes(open(saved_filename, 'rb'))).hexdigest()

        with DBManager() as dbm:
            dbm.insert_meeting_file(meeting_uuid=id, calculated_hash=calculated_hash)

    return json({'status': 'done'})


if __name__ == '__main__':
    p = multiprocessing.Process(target=second_service.worker)
    p.start()
    app.run() # workers=4



