from flask import Flask

app = Flask(__name__)

@app.route('/add-emoji/')
def add_emoji(emoji=None):
        return 'add emoji.'

@app.route('/remove-emoji/')
def remove_emoji(emoji=None):
        return 'remove emoji.'

@app.route('/get-all-dubs/')
def get_emojis(dubs=None):
        return 'get emojies.'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

