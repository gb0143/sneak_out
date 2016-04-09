from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
    
@app.route('/add_event')
def add_event():
    return "add_event code here"
    
@app.route('/add_comment')
def add_comment():
    return "add_comment code here, will need some sort of event_id"

@app.route('/up_vote')
def up_vote():
    return "up_vote code will go here, will need some sort of event_id"

@app.route('/down_vote')
def up_vote():
    return "up_vote code will go here, will need some sort of event_id"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=True)