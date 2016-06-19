from flask import Flask
import requests

app = Flask(__name__)

@app.route('/add-dub/<dub_name>')
def add_dub(dub_name):
    if dub_name:
        r = requests.post('http://172.22.0.4:8182',
                json = {"gremlin": "graph.addVertex('dub', '{}')".format(dub_name)})
        #return r.text
        r_json =  r.json()
        return str(r_json['result']['data'][0]['id'])
    else:
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

