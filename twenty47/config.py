CSRF_ENABLED = True
SECRET_KEY = 'udtu$%gutDu@*IthCaydBip8'
DEBUG=True
MONGODB_SETTINGS = {'DB': 'twenty47', "USERNAME": '247', 'PASSWORD':'twenty47'}

SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
SECURITY_CHANGEABLE = True
SECURITY_EMAIL_SENDER = 'dispatch_report@npexchange.org'

MAIL_USE_SSL = True
MAIL_SERVER = 'email-smtp.us-east-1.amazonaws.com'
MAIL_PORT = 465
MAIL_PASSWORD = 'AsqSErTS/FSi6UO7xLDcJvIYV3G10O0qWSB89x36tHgp'
MAIL_USERNAME = 'AKIAINXNANXPCYMFDQPA'
MAIL_DEBUG = True

DISPATCH_ERROR_GENERAL = "Encountered a problem. Please try again. If this error persists, please contact your administrator."
DISPATCH_ERROR_REMOTEADMIN = "Remote administration failed. Please login to complete your request."


