from django.test import TestCase
from classifier import ml


class EmailClassifierBodyTests(TestCase):
    def test_high_priority_body(self):
        # Generic subject, but urgent body
        subject = "Hello"
        body = "Our database server crashed and the main production app is down. Please fix asap!"
        label, confidence = ml.predict(subject, body)
        self.assertEqual(label, "High")
        self.assertGreater(confidence, 0.5)

    def test_medium_priority_body(self):
        # Generic subject, but routine work body
        subject = "Update"
        body = "Here is the project status update and draft agenda for our Thursday team meeting. Please review."
        label, confidence = ml.predict(subject, body)
        self.assertEqual(label, "Medium")

    def test_low_priority_body(self):
        # Generic subject, but promotional/newsletter body
        subject = "Special Announcement"
        body = "Enjoy 50% off on all items this weekend! Click here to redeem your coupon or unsubscribe."
        label, confidence = ml.predict(subject, body)
        self.assertEqual(label, "Low")

