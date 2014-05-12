from flask import Flask, flash
from flask.ext.mongoengine import MongoEngine
from flask_wtf.csrf import CsrfProtect
from flask_mail import Mail
import blinker

app = Flask(__name__)
app.config.from_object(__name__)

# Load the config
app.config.from_pyfile('local.config.py')

app.config.update(dict(
	DEBUG=True,
))
app.config.from_envvar('config', silent=True)

db = MongoEngine(app)
mail = Mail(app)
csrf = CsrfProtect()
csrf.init_app(app)

"""
Register my signals
"""
twenty47_signals = blinker.Namespace()
subscription_updated = twenty47_signals.signal("subscription-updated")
subscription_pending = twenty47_signals.signal("subscription-pending")
sns_error = twenty47_signals.signal("sns-error")
dispatch_created = twenty47_signals.signal("dispatch-created")

debug = flash

def register_blueprints(app):
    # Prevents circular imports
    from twenty47.views import dispatch
    app.register_blueprint(dispatch)
    from twenty47.admin import admin
    app.register_blueprint(admin)
    from twenty47.admin_dispatch import admin_dispatch
    app.register_blueprint(admin_dispatch)
    from twenty47.subscriber import subscriber
    app.register_blueprint(subscriber)
    
def subscribe_to_signals(app):
    import signals
    
    
register_blueprints(app)
subscribe_to_signals(app)


if __name__ == '__main__':
    app.run()
