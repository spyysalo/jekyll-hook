import os
import json
import smtplib

from email.mime.text import MIMEText

from flask import Flask
from flask import request

from time import strftime

LOGDIR='events'

app = Flask(__name__)

def logevent(s):
    try:
        os.mkdir(LOGDIR)
    except OSError:
        pass
    t = strftime("%Y%m%d%H%M%S")
    fn = os.path.join(LOGDIR, t+'.json')
    with open(fn, 'wt') as f:
        f.write(s)
    return fn

def mailevent(fn):
    with open(fn, 'rb') as f:
        msg = MIMEText(f.read())
    sender = 'sampo.pyysalo@gmail.com'
    receiver = 'sampo.pyysalo@gmail.com'
    msg['Subject'] = 'Jekyll-hook event'
    msg['From'] = sender
    msg['To'] = receiver
    s = smtplib.SMTP('localhost')
    s.sendmail(sender, [receiver], msg.as_string())
    s.quit()

@app.route('/', methods=['POST'])
def event():
    data = json.loads(request.data)

    pretty = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    fn = logevent(pretty)

    mailevent(fn)

    print pretty
    return "OK"

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0')
