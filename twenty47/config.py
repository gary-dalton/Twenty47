# Settings for Flask
CSRF_ENABLED = True
DEBUG = False
# Change these
SECRET_KEY = 'thesecretkey'

# Settings for Flask-Mongoengine
# Change these
MONGODB_SETTINGS = {'DB': 'db_name', "USERNAME": 'db_user', 'PASSWORD':'db_pwd'}

# Settings for Flask-Security
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
SECURITY_PASSWORDLESS = False
SECURITY_CHANGEABLE = True
# Change these
SECURITY_PASSWORD_SALT = 'some_long_string_for_you_to_change'
SECURITY_EMAIL_SENDER = 'email_sender@yourbiz.com'

# Settings for Flask-Mail
# Change these to match your mail server
MAIL_SERVER = 'SMTP Server'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = False
MAIL_USERNAME = 'smtp email user'
MAIL_PASSWORD = 'smtp email pwd'
DEFAULT_MAIL_SENDER = 'email_sender@yourbiz.com'

# Settings for Twenty47
DISPATCH_MAX_TOKEN_AGE = 432000
# Change these
DISPATCH_EMAIL_TOPIC = 'arn:aws:sns:us-zone-1:3456345645756756:Dispatch_Email'
DISPATCH_SMS_TOPIC = 'arn:aws:sns:us-zone-1:3456345645756756:Dispatch_SMS'

# Twenty47 Messages
DISPATCH_ERROR_GENERAL = "Encountered a problem. Please try again. If this error persists, please contact your administrator."
DISPATCH_ERROR_REMOTEADMIN = "Remote administration failed. Please login to complete your request."






