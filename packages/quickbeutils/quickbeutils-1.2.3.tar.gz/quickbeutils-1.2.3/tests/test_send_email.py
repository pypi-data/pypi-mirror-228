import os
import unittest
from datetime import datetime
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from quickbeutils import send_email, SEND_EMAIL_VIA_AWS_SES, SEND_EMAIL_VIA_GMAIL

load_dotenv()

UNIT_TEST_SENDER_EMAIL_ADDRESS = os.getenv('UNIT_TEST_SENDER_EMAIL_ADDRESS')
UNIT_TEST_RECIPIENT_EMAIL_ADDRESS = os.getenv('UNIT_TEST_RECIPIENT_EMAIL_ADDRESS')
UNIT_TEST_REPLY_TO_EMAIL_ADDRESS = os.getenv('UNIT_TEST_REPLY_TO_EMAIL_ADDRESS')
UNIT_TEST_ATTACHMENT_BASE64_A = os.getenv('UNIT_TEST_ATTACHMENT_BASE64_A')
UNIT_TEST_ATTACHMENT_BASE64_B = os.getenv('UNIT_TEST_ATTACHMENT_BASE64_B')


class SendEmailTestCase(unittest.TestCase):

    def test_send_via_aws_ses(self):
        result = send_email(
            sender=UNIT_TEST_SENDER_EMAIL_ADDRESS,
            # reply_to=UNIT_TEST_REPLY_TO_EMAIL_ADDRESS,
            sender_name='Unit Testing',
            recipient=UNIT_TEST_RECIPIENT_EMAIL_ADDRESS,
            subject=f'Unit testing, sent by AWS SES {datetime.now()}',
            body_text='Hello, this is a test.',
            attachments={'image.jpg': UNIT_TEST_ATTACHMENT_BASE64_A, 'lorem.txt': UNIT_TEST_ATTACHMENT_BASE64_B},
            send_via=SEND_EMAIL_VIA_AWS_SES
        )
        self.assertEqual(True, result)

    def test_send_via_gmail(self):
        result = send_email(
            sender=UNIT_TEST_SENDER_EMAIL_ADDRESS,
            sender_name='Unit Testing',
            recipient=UNIT_TEST_RECIPIENT_EMAIL_ADDRESS,
            subject=f'Unit testing, sent by gmail {datetime.now()}',
            body_text='Hello, this is a test.',
            send_via=SEND_EMAIL_VIA_GMAIL
        )
        self.assertEqual(True, result)


if __name__ == '__main__':
    unittest.main()
