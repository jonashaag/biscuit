from os import chdir
from smtplib import SMTP
from urlparse import parse_qs
from json import loads

from nano import NanoApplication

import config

app = NanoApplication(debug=True)

@app.route('/postcommithook/')
def postcommithook(environ):
    payload = parse_qs(environ['wsgi.input'].read())['payload'][0]
    meta = loads(payload)
    for commit in meta['commits']:
        err = config.run()
        if err is None:
            send_mail("Successfully built/tested %s at revision %s" %
                      (config.PROJECT_NAME, commit['id']))
        else:
            send_mail("Building/testing %s at revision %s failed:\n\n%s" %
                      (config.PROJECT_NAME, commit['id'], err))
    return 'yo build done'

def send_mail(body):
    smtp = SMTP(config.EMAIL_SENDER_HOST)
    payload = '\r\n'.join([
        'From: Biscuit <%s>' % config.EMAIL_SENDER_EMAIL,
        'To: %s' % config.EMAIL_RECEIVER,
        'Subject: %s biscuit report' % config.PROJECT_NAME,
        '', body
    ])
    smtp.sendmail(config.EMAIL_SENDER_EMAIL, [config.EMAIL_RECEIVER], payload)
    smtp.quit()

if __name__ == '__main__':
    import bjoern
    bjoern.run(app, '0.0.0.0', 8080)
