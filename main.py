from flask import Flask, jsonify, request
import i3_mgmt
import requests
import json

app = Flask(__name__)
i3 = i3_mgmt.i3MGMT

try:
    config_f = open('config.json')
except FileNotFoundError:
    config = json.dumps({'server ip': input('Server IP: '), 'device name': input('Device Name: ')}, indent=4)
    config_f = open('config.json', 'x')
    config_f.write(config)
    config_f.close()
else:
    config = json.loads(config_f.read())
    config_f.close()

def contact_server(path, method, data=None):
    if method == 'GET':
        r = requests.get('http://{}:4861{}'.format(config['server ip'], path))
    elif method == 'POST':
        r = requests.post('http://{}:4861{}'.format(config['server ip'], path), data=data)
    resp = json.loads(r.content.decode('utf-8'))
    if resp['code'] == 200:
        return resp
    else:
        raise Exception('Server returned {} {}'.format(resp['code'], resp['data']))

@app.errorhandler(500)
def handle500(e):
    return jsonify({
        'code': 500,
        'data': 'Internal Server Error'
    })

@app.errorhandler(404)
def handle404(e):
    return jsonify({
        'code': 404,
        'data': 'Not found'
    })

@app.errorhandler(400)
def handle400(e):
    return jsonify({
        'code': 400,
        'data': 'Bad request'
    })

@app.errorhandler(405)
def handle400(e):
    return jsonify({
        'code': 405,
        'data': 'Method Not Allowed'
    })

@app.route('/ping')
def ping():
    return jsonify({
        'code': 200,
        'data': 'pong'
    })

@app.route('/announcement', methods=['POST'])
def announcement():
    i3.nag('New Announcement From {}: {}'.format(request.form['from'], request.form['data']))
    return jsonify({
        'code': 200,
        'data': 'OK'
    })

if __name__ == '__main__':
    id = contact_server('/add_client', 'POST', data={'name': config['device name']})['id']
    app.dev_id = id
    app.run(host='0.0.0.0', port=4860)
