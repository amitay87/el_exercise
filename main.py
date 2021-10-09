import hashlib
import urllib.request

from sanic import Sanic
from sanic.response import json
# import requests


app = Sanic("My Hello, world app")

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



# TODO: consider handling requests asyncronously
@app.route('/notify_record_completion', methods=['POST'])
async def test(request): # TODO: refactor function name

    print(f"AAA request.body: {request.body}")

    recording_files = request.json['payload']['object']['recording_files']
    download_urls = [rf['download_url'] for rf in recording_files]
    print(f"AAA download_urls: {download_urls}")

    for file in recording_files:
        extension = file['file_extension']
        id = file['id']
        saved_filename = f"{id}.{extension}"
        # TODO: consider making the requests asyncronously
        urllib.request.urlretrieve(file['download_url'], saved_filename)
        # TODO: consider calculating hash asyncronously
        print(hashlib.md5(file_as_bytes(open(saved_filename, 'rb'))).hexdigest())

    return json({'hello': 'world'})

if __name__ == '__main__':
    app.run()