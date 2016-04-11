from flask import Flask, request
from pymongo import MongoClient
from dateutil import parser
import pytz, datetime
from bson.objectid import ObjectId
import urllib3

app = Flask(__name__)

db  = MongoClient()["sneakoutdb"]
# print db
#db.collection.ensureIndex( { "startTime": 1, "endTime": 1, "lat": 1, "lng": 1, "eventName": 1, "eventType": 1 }, {unique:true} )
event_table = db["events"]
print event_table
# event_table.remove();
print event_table.count()

@app.route('/')
def hello_world():
    return "Hello World!"
    
@app.route('/add_event')
def add_event():
    event_name = request.args['name']
    location_lat = float(request.args['lat'])
    if(location_lat > 90 or location_lat < -90):
        return "bad lattitude"
    location_lng = float(request.args['lng'])
    if(location_lng > 180 or location_lat < -180):
        return "bad longitude"
    start_time = to_utc(request.args['start'])
    end_time = to_utc(request.args['end'])
    if(end_time <= start_time):
        return "invalid request"
    event_type = request.args['type']
    image_url='https://www.originvietnam.com/file/st_uploadfont/No_Image.jpg'
    if('image' in request.args):
        image_url = request.args['image']
        try: 
            print urllib3.urlopen(image_url)
        except:
            return image_url + "  site does not exist"
            
    #Add to mongo here...
    try:
        event_table.insert({"startTime": start_time, "endTime": end_time, "lat":location_lat, "lng": location_lng, "name":event_name, "votes":0, "comments":[], "type":event_type, "imageLink":image_url})
        print event_table.find_one()
        return "Inserting entry: " + str(event_table.count())
    except:
        return "Could not insert, duplicate entry"
    return "add_event code here"
    
def to_utc(date_string):
    return parser.parse(date_string).astimezone(pytz.utc)
    
@app.route('/add_comment')
def add_comment():
    comment = request.args['comment']
    event_id = ObjectId(request.args['event_id'])
    event_table.update({'_id': event_id}, {'$push': {
            'comments' : comment
            }
        })
    print event_table.find_one({'_id': event_id})
    return "add_comment"

@app.route('/up_vote')
def up_vote():
    event_id = ObjectId(request.args['event_id'])
    event_table.update({'_id': event_id}, {'$inc': {
            'votes' : 1
            }
    })
    print event_table.find_one({'_id': event_id})
    return "upvoted!"

@app.route('/down_vote')
def down_vote():
    event_id = ObjectId(request.args['event_id'])
    event_table.update({'_id': event_id}, {'$inc': {
            'votes' : -1
            }
    })
    print event_table.find_one({'_id': event_id})
    return "downvoted!"

@app.route('/query')
def search():
    top_left_lat = float(request.args['tl_lat'])
    if(top_left_lat > 90 or top_left_lat < -90):
        return "bad lattitude"
        
    top_left_lng = float(request.args['tl_lng'])
    if(top_left_lng > 180 or top_left_lng < -180):
        return "bad longitude"
    
    bottom_right_lat = float(request.args['br_lat'])
    if(bottom_right_lat > 90 or bottom_right_lat < -90):
        return "bad lattitude"
    bottom_right_lng = float(request.args['br_lng'])
    if(bottom_right_lng > 180 or bottom_right_lng < -180):
        return "bad longitude"
    
    start_time = to_utc(request.args['start'])
    # end_time = to_utc(request.args['end'])
    # if(end_time <= start_time):
    #     return "invalid request"
    
    print("top_left_lat: " + str(top_left_lat))
    
    cursor = event_table.find({'startTime':{'$gte':start_time}, 'lat': { '$gt' : bottom_right_lat, '$lt' : top_left_lat}, 'lng': { '$gt' : bottom_right_lng, '$lt' : top_left_lng}})
    # cursor = event_table.find({'startTime':{'$gte':start_time}})
    print cursor.count();
    return "something"
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=True)