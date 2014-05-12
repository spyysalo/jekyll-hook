import os
import json
import subprocess
import smtplib
import logging

from time import strftime
from glob import glob

from email.mime.text import MIMEText

from flask import Flask
from flask import request

# port to listen to
PORT = 5836

# directory to log github webhook events to. Set LOG_DIR = None to
# disable event logging.
LOG_DIR='events'

# sender and receiver for email notifications. Set EMAIL_RECEIVER =
# None to disable email notifications.
EMAIL_SENDER = 'sampo.pyysalo@gmail.com'
EMAIL_RECEIVER = 'sampo.pyysalo@gmail.com'

# directory where to run scripts from. Set SCRIPT_DIR = None to
# disable scripts.
SCRIPT_DIR = 'scripts'

# Warning: never leave DEBUG = True when deploying: this flag is
# propagated to Flask app debug, which can allow for arbitrary code
# execution.
DEBUG = False

# configure logging
if DEBUG:
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(funcName)s: %(message)s')

app = Flask(__name__)

def log_event(s):
    if LOG_DIR is None:
        return None

    # assure that LOG_DIR exists
    try:
        os.mkdir(LOG_DIR)
    except OSError:
        pass

    # derive filename from time
    t = strftime("%Y%m%d%H%M%S")
    fn = os.path.join(LOG_DIR, t+'.json')

    try:
        with open(fn, 'wt') as f:
            f.write(s)
    except Exception, e:
        logging.error('failed to write {}: {}', fn, e)

    return fn

def mail_file(fn, subject, sender=EMAIL_SENDER, receiver=EMAIL_RECEIVER):
    if fn is None or sender is None:
        return None

    with open(fn, 'rb') as f:
        msg = MIMEText(f.read())

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    s = smtplib.SMTP('localhost')
    s.sendmail(sender, [receiver], msg.as_string())
    s.quit()

def commit_author(data):
    try:
        return data['commits'][0]['author']['name']
    except Exception:
        return None

def send_email(fn, data):
    author = commit_author(data)
    if author is None:
        subject = 'Jekyll-hook: event'
    else:
        subject = 'Jekyll-hook: commit by {}'.format(author)
    mail_file(fn, subject)

def pretty_print_json(data):
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

def load_json(source):
    try:
        data = json.loads(source)
    except Exception, e:
        logging.error('failed to load json from {}: {}'.format(source, e))
        raise
    return data

def run_script(script):
    logging.info('running {}'.format(script))
    try:
        p = subprocess.Popen(script, stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE)
        out, err = p.communicate() 
    except Exception, e:
        logging.error('failed to run {}: {}'.format(script, e))
        raise

    if out:
        logging.info('{}:OUT: {}'.format(script, out))
    if err:
        logging.error('{}:ERR: {}'.format(script, err))

    logging.info('completed {}'.format(script))

def run_scripts(directory=SCRIPT_DIR):
    if directory is None:
        return None

    scripts = glob(os.path.join(directory, '*.sh'))

    for script in scripts:
        run_script(script)

@app.route('/', methods=['POST'])
def event():
    data = load_json(request.data)
    
    fn = log_event(pretty_print_json(data))

    send_email(fn, data)

    run_scripts()

    return "OK"

if __name__ == '__main__':
    if DEBUG:
        app.debug = True
    app.run(host='0.0.0.0', port=PORT)
