# import json
from sanic.response import json

from sanic import Sanic

import db

def worker():
    print("AAA in worker()")
    app = Sanic("second_service")

    @app.route('/get_calculated_hash/<meeting_uuid>', methods=['GET'])
    async def get_calculated_hash(request, meeting_uuid): # TODO: refactor function name
        print(f"AAA request,  meeting_uuid: {request, meeting_uuid}")
        conn = db.get_connection()
        calculated_hash = db.get_calculated_hash(conn, meeting_uuid)
        print(f"AAA calculated_hash: {calculated_hash}")
        return json({'calculated_hash': calculated_hash})

    app.run(port=8002)

if __name__ == '__main__':
    pass
    # app.run(port=8002)