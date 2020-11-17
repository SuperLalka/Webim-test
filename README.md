# Webim-test
Test application with OAuth authentication and generation of random numbers that are the same for all users.
# Requirements
The project was built in Django using the following requirements:
- oauth2_provider,
- corsheaders,
- channels,
- django_celery_results

It also needs a running redis-server and one / two Celery workers to work, eg.:
- celery -A webim worker -l info -B
