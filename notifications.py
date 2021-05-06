"""Notifications module."""
import constants
import requests

BASE_URL = 'https://api.mailgun.net/v3/'

def email(subject, body):
    """Send an email notification.

    :param alert: name of alert
    :param body: email contents
    """
    # send via Mailgun
    response = requests.post(BASE_URL + constants.MAILGUN_DOMAIN + '/messages',
                             auth=('api', constants.MAILGUN_API_KEY),
                             data={'from': f'BitBot v2 Notifier <noreply@{constants.MAILGUN_DOMAIN}>',
                                   'to': [constants.EMAIL_ADDRESS],
                                   'subject': subject,
                                   'text': body})

    # handle failure
    if response.status_code != 200:
        try:
            message = response.json().get('message', '<none>')
        except Exception as error:
            message = repr(error)
        print(f'Mailgun alert failed: {message} ({response.status_code})')
