import os, sys, inspect, random, string
import twenty47
import unittest
import tempfile
import twenty47.utils as utils

import boto

# Need to use the local moto for proper NextToken
cmd_folder = '/home/gary/projects/moto'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from moto import mock_sns

@unittest.skip("Skip over the entire test routine") 
class TestMocking(unittest.TestCase):
    @mock_sns
    def test_create_topic(self):
        conn = boto.connect_sns()
        conn.create_topic("some-topic")

        topics_json = conn.get_all_topics()
        topics = topics_json["ListTopicsResponse"]["ListTopicsResult"]["Topics"]
        self.assertEqual(len(topics), 1)
        self.assertEqual(topics[0]['TopicArn'], "arn:aws:sns:us-east-1:123456789012:some-topic")
        
        
        # Delete the topic
        conn.delete_topic(topics[0]['TopicArn'])

        # And there should now be 0 topics
        topics_json = conn.get_all_topics()
        topics = topics_json["ListTopicsResponse"]["ListTopicsResult"]["Topics"]
        self.assertEqual(len(topics), 0)
        
    @mock_sns
    def test_creating_subscription(self):
        conn = boto.connect_sns()
        conn.create_topic("some-topic")
        topics_json = conn.get_all_topics()
        topic_arn = topics_json["ListTopicsResponse"]["ListTopicsResult"]["Topics"][0]['TopicArn']

        conn.subscribe(topic_arn, "http", "http://example.com/")

        subscriptions = conn.get_all_subscriptions()["ListSubscriptionsResponse"]["ListSubscriptionsResult"]["Subscriptions"]
        self.assertEqual(len(subscriptions), 1)
        subscription = subscriptions[0]
        self.assertEqual(subscription["TopicArn"], topic_arn)
        self.assertEqual(subscription["Protocol"], "http")
        self.assertIn(topic_arn, subscription["SubscriptionArn"])
        self.assertEqual(subscription["Endpoint"], "http://example.com/")

        # Now unsubscribe the subscription
        conn.unsubscribe(subscription["SubscriptionArn"])

        # And there should be zero subscriptions left
        subscriptions = conn.get_all_subscriptions()["ListSubscriptionsResponse"]["ListSubscriptionsResult"]["Subscriptions"]
        self.assertEqual(len(subscriptions), 0)
    

#@unittest.skip("Skip over the entire test routine") 
class TestUtils(unittest.TestCase):
    @mock_sns
    def setUp(self):
        self.db_fd, twenty47.app.config['DATABASE'] = tempfile.mkstemp()
        twenty47.app.config['TESTING'] = True
        self.app = twenty47.app.test_client()
        self.conn = boto.connect_sns()
        #twenty47.init_db()
        self.email_topic = 'Dispatch_Email'
        self.email_arn = 'arn:aws:sns:us-east-1:123456789012:Dispatch_Email'
        self.sms_topic = 'Dispatch_SMS'
        self.sms_arn = 'arn:aws:sns:us-east-1:123456789012:Dispatch_SMS'
        self.email_endpoint = 'test@test.com'
        self.sms_endpoint = '14145555555'
        
    @mock_sns
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(twenty47.app.config['DATABASE'])
        
    @mock_sns
    #@unittest.skip("Skip over the entire test routine") 
    def test_put_subscriber(self):
        self.create_topics(self.conn)
        self.email_subscription_arn =  utils.put_subscriber(twenty47.app.config['DISPATCH_EMAIL_TOPIC'], 'email' , self.email_endpoint, self.conn)
        self.sms_subscription_arn =  utils.put_subscriber(twenty47.app.config['DISPATCH_SMS_TOPIC'], 'sms' , self.sms_endpoint, self.conn)
        self.assertGreater(len(self.email_subscription_arn), 80)
        self.assertGreater(len(self.sms_subscription_arn), 80)
        
    @mock_sns      
    def test_get_one_subscriber(self):
        self.create_topics(self.conn)
        for i in range(212):
            utils.put_subscriber(twenty47.app.config['DISPATCH_EMAIL_TOPIC'], 'email' , str(i) + self.email_endpoint, self.conn)
            
        response = utils.get_one_subscriber(twenty47.app.config['DISPATCH_EMAIL_TOPIC'], '1' + self.email_endpoint, None, self.conn)
        print('1' + self.email_endpoint + ' EQUALS ' + response['Endpoint'])
        self.assertEqual('1' + self.email_endpoint, response['Endpoint'])
        
        response = utils.get_one_subscriber(twenty47.app.config['DISPATCH_EMAIL_TOPIC'], '201' + self.email_endpoint, None, self.conn)
        print('201' + self.email_endpoint + ' EQUALS ' + response['Endpoint'])
        self.assertEqual('201' + self.email_endpoint, response['Endpoint'])
        
        response = utils.get_one_subscriber(twenty47.app.config['DISPATCH_EMAIL_TOPIC'], '250' + self.email_endpoint, None, self.conn)
        print('250' + self.email_endpoint + ' FALSE, NOT FOUND ' + str(response))
        self.assertFalse(response)
        
    @mock_sns      
    def test_del_subscriber(self):
        self.create_topics(self.conn)
        for i in range(10):
            utils.put_subscriber(twenty47.app.config['DISPATCH_SMS_TOPIC'], 'sms' , str(i) + self.sms_endpoint, self.conn)
        
        response = utils.get_one_subscriber(twenty47.app.config['DISPATCH_SMS_TOPIC'], '1' + self.sms_endpoint, None, self.conn)
        print('1' + self.sms_endpoint + ' EQUALS ' + response['Endpoint'])
        self.assertEqual('1' + self.sms_endpoint, response['Endpoint'])
        
        response = utils.del_subscriber(response['SubscriptionArn'], self.conn)
        print('True means successfully deleted: %s' % (response))
        self.assertTrue(response)
        
        response = utils.get_one_subscriber(twenty47.app.config['DISPATCH_SMS_TOPIC'], '1' + self.sms_endpoint, None, self.conn)
        print('1' + self.sms_endpoint + ' FALSE, NOT FOUND ' + str(response))
        self.assertFalse(response)
        
    @mock_sns
    def test_get_topic_subscribers(self):
        self.create_topics(self.conn)
        
        for i in range(10):
            utils.put_subscriber(twenty47.app.config['DISPATCH_EMAIL_TOPIC'], 'email' , str(i) + self.email_endpoint, self.conn)
        for i in range(12):
            utils.put_subscriber(twenty47.app.config['DISPATCH_SMS_TOPIC'], 'sms' , str(i) + self.sms_endpoint, self.conn)
            
        response = utils.get_topic_subscribers(twenty47.app.config['DISPATCH_EMAIL_TOPIC'], conn=self.conn)
        self.assertEqual(len(response), 10)
                
        response = utils.get_topic_subscribers(twenty47.app.config['DISPATCH_SMS_TOPIC'], conn=self.conn)
        self.assertEqual(len(response), 12)
        
        # Test get_all_subscribers()
        all_response = utils.get_all_subscribers(self.conn)
        self.assertEqual(len(all_response), 22)
        
        for k, subscriptionArn in response.items():
             utils.del_subscriber(subscriptionArn, self.conn)
        response = utils.get_topic_subscribers(twenty47.app.config['DISPATCH_SMS_TOPIC'], conn=self.conn)
        print response
        self.assertEqual(len(response), 0)
        
        
    @mock_sns
    def test_put_sns_message(self):
        self.create_topics(self.conn)
        
        message = ''.join(random.choice(string.lowercase) for x in range(200))
        response = utils.put_sns_sms_message(message, self.conn)
        print response
        self.assertEqual(len(response), 0)
        
        response = utils.put_sns_message(twenty47.app.config['DISPATCH_EMAIL_TOPIC'], message, conn=self.conn)
        print response
        self.assertEqual(len(response), 0)
        
      
        
        
        
        


        
    @mock_sns
    def create_topics(self, conn):
        conn.create_topic(self.email_topic)
        conn.create_topic(self.sms_topic)
        topics_json = conn.get_all_topics()
        twenty47.app.config['DISPATCH_EMAIL_TOPIC'] = topics_json["ListTopicsResponse"]["ListTopicsResult"]["Topics"][0]['TopicArn']
        self.assertEqual(twenty47.app.config['DISPATCH_EMAIL_TOPIC'], self.email_arn)
        twenty47.app.config['DISPATCH_SMS_TOPIC'] = topics_json["ListTopicsResponse"]["ListTopicsResult"]["Topics"][1]['TopicArn']
        self.assertEqual(twenty47.app.config['DISPATCH_SMS_TOPIC'], self.sms_arn)
               
