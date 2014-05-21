import os
import twenty47
import unittest
import tempfile

class Twenty47TestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, twenty47.app.config['DATABASE'] = tempfile.mkstemp()
        twenty47.app.config['TESTING'] = True
        self.app = twenty47.app.test_client()
        twenty47.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(twenty47.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
""" 

   
"""

"""

import random
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

if __name__ == '__main__':
    unittest.main()
    


class 
    
from boto import sns


mail = Mail(app)
conn = sns.SNSConnection()

def get_one_subscriber(topic, endpoint, nexttoken=None):
    '''
    Returns False or the subscription data:
    {'Owner': '796928799269', 'Endpoint': 'gary@gruffgoat.com', 'Protocol': 'email', 'TopicArn': 'arn:aws:sns:us-east-1:796928799269:Dispatch_Email', 'SubscriptionArn': 'arn:aws:sns:us-east-1:796928799269:Dispatch_Email:784fe2e3-f495-4c63-85e2-2306c2b400df'}
    '''
    try:
        subscribers_obj = conn.get_all_subscriptions_by_topic(topic, nexttoken)
        for subscriber in subscribers_obj['ListSubscriptionsByTopicResponse']['ListSubscriptionsByTopicResult']['Subscriptions']:
            if subscriber['Endpoint'] == endpoint:
                return subscriber
        if subscribers_obj['ListSubscriptionsByTopicResponse']['ListSubscriptionsByTopicResult']['NextToken'] == None:
            return False
        else:
            return get_one_subscriber(topic, endpoint, nexttoken)
    except Exception, e:
        sns_error.send(app, func='get_email_subscribers', e=e)
    return False
    
"""
