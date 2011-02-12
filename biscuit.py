from os import chdir
from shutil import rmtree
from tempfile import mkdtemp
from smtplib import SMTP
from json import loads

from nano import NanoApplication

import config

app = NanoApplication(debug=True)

@app.route('/postcommithook/')
def postcommithook(environ):
    meta = loads(environ['wsgi.input'].read())
    for commit in meta['commits']:
        tempdir = mkdtemp()
        try:
            err = config.run(tempdir)
            if err is None:
                send_mail("Successfully built/tested %s at revision %s" %
                          (config.PROJECT_NAME, commit['id']))
            else:
                send_mail("Building/testing %s at revision %s failed:\n\n%s" %
                          (config.PROJECT_NAME, commit['id'], err))
        finally:
            rmtree(tempdir)

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
