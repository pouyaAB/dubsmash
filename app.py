from flask import Flask
from flask import request
import time
import requests
from operator import itemgetter
from collections import defaultdict

app = Flask(__name__)

@app.route('/remove')
def remove():
    r = requests.post('http://172.22.0.4:8182',
            json = {"gremlin": "g.V().drop().iterate()"})
    return r.text

@app.route('/parse')
def parse():
    r = requests.post('http://172.22.0.4:8182',
            json = {"gremlin": "g.V().has('dub').inE('react')"})
    reacts = r.json()['result']['data']
    #return r.text
    react_dict = {}
    react_max = {}
    react_list = []
    react_return_list = []
    for react in reacts:
        if react['inV'] in react_dict:
            react_dict[react['inV']].append((react['properties']['emoji'], react['properties']['timestamp']))
        else:
             react_dict[react['inV']] = []
             react_dict[react['inV']].append((react['properties']['emoji'], react['properties']['timestamp']))
    for key, value in react_dict.iteritems():
        react_max[key] = max(value, key=itemgetter(1))[1]
    react_max = sorted(react_max.items(), key=itemgetter(1), reverse=True)
    for react in react_max:
        react_list.append((react[0], react_dict[react[0]]))
    for react in react_list:
        emoj_dict = defaultdict(int)
        tuple_list = react[1]
        for emoj in tuple_list:
            emoj_dict[emoj[0]] += 1
        react_return_list.append((react[0], emoj_dict))
    return str(react_return_list)


@app.route('/sort-dub')
def sort_dub():
    r = requests.post('http://172.22.0.4:8182',
            json = {"gremlin": "g.V().has('dub').inE('react').values('timestamp')"})
    return r.text

@app.route('/add-dub/<dub_name>')
def add_dub(dub_name):
    if dub_name:
        r = requests.post('http://172.22.0.4:8182',
                json = {"gremlin": "graph.addVertex('dub', '{}')".format(dub_name)})
        r_json =  r.json()
        if 'result' in r_json and 'data' in r_json['result'] and (len(r_json['result']['data']) == 1) and\
                'id' in r_json['result']['data'][0]:
            return str(r_json['result']['data'][0]['id'])
        else:
            return '400'
    return "404"

@app.route('/add-user/<user_name>')
def add_user(user_name):
    if user_name:
        r = requests.post('http://172.22.0.4:8182',
                json = {"gremlin": "graph.addVertex('user', '{}')".format(user_name)})
        r_json =  r.json()
        return str(r_json['result']['data'][0]['id'])
    else:
        return "404"

@app.route('/react', methods=['GET'])
def react():
    dub_id = request.args.get('dub_id')
    user_name = request.args.get('user_name')
    emoji_string = request.args.get('emoji_string')
    if user_name and dub_id and emoji_string:
        check_in_db = requests.post('http://172.22.0.4:8182',
                json = {"gremlin": "g.V('{}').inE('react').has('emoji', '{}')\
                        .outV().has('user', '{}').count()".format(dub_id, emoji_string, user_name)})
        if check_in_db.json()['result']['data'][0] == 0:
            timestamp = str(time.time())
            r = requests.post('http://172.22.0.4:8182',
                    json = {"gremlin": "v1=g.V('{}').next(); v2=g.V().has('user', '{}').next();\
                        e1=v2.addEdge('react', v1, 'emoji', '{}', 'timestamp', '{}')"\
                        .format(dub_id, user_name, emoji_string, timestamp)})
            return r.text

    return "404"

@app.route('/all-dubs/')
def list_all_dubs():
    r = requests.post('http://172.22.0.4:8182',
            json = {"gremlin": "g.V()"})
    r_json =  r.json()
    dubs = {}
    #return str(r.text)
    if 'result' in r_json and 'data' in r_json['result']:
        dubs_list = r_json['result']['data']
        for dub in dubs_list:
            if 'properties' in dub and 'dub' in dub['properties']:
                dubs_obj = dub['properties']
                dubs[dub['id']] = dubs_obj['dub'][0]['value']

    return str(dubs)

@app.route('/all-users/')
def list_all_users():
    r = requests.post('http://172.22.0.4:8182',
            json = {"gremlin": "g.V()"})
    r_json =  r.json()
    users = {}
    #return str(r.text)
    if 'result' in r_json and 'data' in r_json['result']:
        users_list = r_json['result']['data']
        for user in users_list:
            if 'properties' in user and 'user' in user['properties']:
                user_obj = user['properties']
                users[user['id']] = user_obj['user'][0]['value']

    return str(users)


@app.route('/add-emoji/')
def add_emoji(emoji=None):
    return requests.post('titan:8182',
            json = {"gremlin": "graph.addvertex({}:)"})

@app.route('/remove-emoji/')
def remove_emoji(emoji=None):
        return 'remove emoji.'

@app.route('/get-all-dubs/')
def get_emojis(dubs=None):
        return 'get emojies.'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

