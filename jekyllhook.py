from flask import Flask
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def event():
    try:
        data = json.loads(request.data)
        print data
    except:
        print "Error loading json:", request.data
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
