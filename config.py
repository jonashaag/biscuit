PROJECT_NAME = 'project1234'
EMAIL_SENDER_HOST = '127.0.0.1'
EMAIL_SENDER_EMAIL = 'noreply@example.org'
EMAIL_RECEIVER = 'john@wayne.tld'

def run():
    test_failures = run_tests()
    if not test_failures:
        # return None to indicate everything's fine.
        return None
    else:
        # if something went wrong, return a string that is included in the mail.
        return '%d failures' % len(test_failures)
