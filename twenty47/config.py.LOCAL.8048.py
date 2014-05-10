CSRF_ENABLED = True
SECRET_KEY = 'thesecretkey'
DEBUG=False
MONGODB_SETTINGS = {'DB': 'db_name', "USERNAME": 'db_user', 'PASSWORD':'db_pwd'}

SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
SECURITY_CHANGEABLE = True
SECURITY_EMAIL_SENDER = 'email_sender@yourbiz.com'

MAIL_USE_SSL = True
MAIL_SERVER = 'SMTP Server'
MAIL_PORT = 465
MAIL_PASSWORD = 'smtp email pwd'
MAIL_USERNAME = 'smtp email user'
MAIL_DEBUG = False

DISPATCH_ERROR_GENERAL = "Encountered a problem. Please try again. If this error persists, please contact your administrator."
DISPATCH_ERROR_REMOTEADMIN = "Remote administration failed. Please login to complete your request."


