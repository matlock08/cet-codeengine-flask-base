import flask
import json
import jwt
import logging
import os
import queue
import re
import requests
import threading
import time


PORT = os.getenv('PORT', '8080')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

# Enrichment task queue
q = queue.Queue()

app = flask.Flask(__name__)
app.logger.setLevel(logging.INFO)
app.logger.handlers[0].setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s (%(filename)s:%(lineno)d)'))


def enrichment_worker():
    while True:
        item = q.get()
        
        try:
            
            app.logger.info('Pulled a batch:')

        except Exception as e:
            app.logger.error('An error occurred: %s', e, exc_info=True)
            # Retry
            q.put(item)

# Turn on the enrichment worker thread
threading.Thread(target=enrichment_worker, daemon=True).start()

# Webhook endpoint
@app.route('/webhook', methods=['GET','POST'])
def webhook():
    # Verify JWT token
    header = flask.request.headers.get('Authorization')
    if not header:
        code = 400
        status = 'missing jwt token'
        return {'status': status}, code

    if not WEBHOOK_SECRET:
        code = 500
        status = 'missing configuration'
        return {'status': status}, code

    
    try:
        _, token = header.split()
        jwt.decode(token, WEBHOOK_SECRET, algorithms=['HS256'])
    except jwt.PyJWTError as e:
        app.logger.error('Invalid token: %s', e)
        return {'status': 'unauthorized'}, 401

    # Process webhook event
    data = flask.json.loads(flask.request.data)
    app.logger.info('Received event: %s', data)

    
    # Receive this event when a batch of the documents gets ready
    code = 202
    status = 'accepted'
    # Put an enrichment request into the queue for async processing
    q.put(data)
        
    return {'status': status}, code

# Webhook endpoint
@app.route('/', methods=['GET'])
def landing():
    # Receive this event when a batch of the documents gets ready
    code = 200
    status = True

    app.logger.info('Received / request')
            
    return  json.dumps({'success':status}), code, {'ContentType':'application/json'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(PORT))
