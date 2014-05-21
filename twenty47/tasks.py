from celery import Celery
from twenty47 import db, app

celery_app = make_celery(app)


def make_celery(app):
    celery = Celery('myapp')

    #celery.config_from_object(app.config)

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'], backend =app.config['CELERY_RESULT_BACKEND'] )
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
    


@celery_app.task
def add(x, y):
    return x + y


@celery_app.task
def print_hello():
    print 'hello there'
    
# Call function using
# gen_prime.delay(x)
    
@celery_app.task
def gen_prime(x):
    multiples = []
    results = []
    for i in xrange(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in xrange(i*i, x+1, i):
                multiples.append(j)
    return results


@celery_app.task
def update_user_subscriptions(user):
    if not user.subscription:
        debug("Why are we here")
        return False
    else:
        if user.subscription.email:
            if get_one_subscriber(app.config['DISPATCH_EMAIL_TOPIC'], user.subscription.email)
            
            current_subscribers = get_email_subscribers()
            try:
                user.subscription.email_arn = current_subscribers[user.subscription.email]
                if user.subscription.status != "APPROVED" or (user.subscription.methods != "Both" and user.subscription.methods != "Email"):
                    del_email_subscriber(user.subscription.email_arn)
                    user.subscription.email_arn = ''
            except KeyError:
                if user.subscription.status == "APPROVED":
                    if user.subscription.methods == "Both" or user.subscription.methods == "Email":
                        user.subscription.email_arn = put_email_subscriber(user.subscription.email)
                        
        if user.subscription.smsPhone:
            current_subscribers = get_sms_subscribers()
            try:
                user.subscription.sms_arn = current_subscribers['1' + user.subscription.smsPhone]
                if user.subscription.status != "APPROVED" or (user.subscription.methods != "Both" and user.subscription.methods != "SMS Phone"):
                    del_sms_subscribers('1' + user.subscription.smsPhone)
                    user.subscription.sms_arn = ''
            except KeyError:
                if user.subscription.status == "APPROVED":
                    if user.subscription.methods == "Both" or user.subscription.methods == "SMS Phone":
                        user.subscription.sms_arn = put_sms_subscriber('1' + user.subscription.smsPhone)

    user.save()
    return True
