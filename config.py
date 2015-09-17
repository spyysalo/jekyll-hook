# port to listen to
PORT=5836

# directory to log github webhook events to. Set LOG_DIR = None to
# disable event logging.
LOG_DIR='events'

# sender and receiver for email notifications. Set EMAIL_RECEIVER =
# None to disable email notifications.
#
# Please define these again in config_site.py
EMAIL_SENDER = 'nobody@nothing.com'
EMAIL_RECEIVER = 'nobody@nothing.com'
SMTP_SERVER = 'someserver.com'

# directory where to run scripts from. Set SCRIPT_DIR = None to
# disable scripts.
SCRIPT_DIR = 'scripts'


###################
# override defaults with local values, if any
try:
    from config_site import *
except:
    pass

