import hashlib
import multiprocessing
import urllib.request

from sanic import Sanic
from sanic.response import json
# import requests
import grequests

from db import DBManager
import second_service
import json as python_json


app = Sanic("handle notify app")

def file_as_bytes(file):
    with file:
        return file.read()

# TODO: consider using this function:
# def md5(fname):
#     hash_md5 = hashlib.md5()
#     with open(fname, "rb") as f:
#         for chunk in iter(lambda: f.read(4096), b""):
#             hash_md5.update(chunk)
#     return hash_md5.hexdigest()


@app.route('/notify_record_completion', methods=['POST'])
async def handle_notify_record_completion(request): # TODO: refactor function name

    print(f"AAA request.body: {request.body}")
    body_json = python_json.loads(str(request.body).replace('\'', '\"')[2:-1])

    recording_files = body_json['payload']['object']['recording_files']
    print(f"AAA recording_files: {recording_files}")
    urls = [rf['download_url'] for rf in recording_files]
    print(f"AAA urls: {urls}")
    rs = (grequests.get(u) for u in urls)
    print(f"AAA rs: {rs}")
    downloads = grequests.map(rs)
    print(f"AAA downloads: {downloads}")


    print(f"AAA download_urls: {urls}")

    for idx, file in enumerate(recording_files):
        extension = file['file_extension']
        id = file['id']
        saved_filename = f"{id}.{extension}"

        with open(saved_filename, 'ab') as f:
                print(downloads[idx].status_code)
                f.write(downloads[idx].content)


        # TODO: consider calculating hash asyncronously
        calculated_hash = hashlib.md5(file_as_bytes(open(saved_filename, 'rb'))).hexdigest()
        print(calculated_hash)

        with DBManager() as dbm:
            dbm.insert_meeting_file(meeting_uuid=id, calculated_hash=calculated_hash)

    return json({'status': 'done'})



if __name__ == '__main__':
    jobs = []

    p = multiprocessing.Process(target=second_service.worker)
    jobs.append(p)
    p.start()
    app.run() # workers=4



