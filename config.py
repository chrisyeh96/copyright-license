import os
import stripe

# Miscellaneous
DEBUG = os.environ.get('DEBUG', False)
TOKEN_URI = '/oauth/token'

# Database
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# File Upload
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = '/tmp/copyright'
REDIS_URL = os.environ.get('REDIS_URL')

# Stripe
SITE = 'https://connect.stripe.com'
CLIENT_ID = os.environ.get('CLIENT_ID')
STRIPE_SECRET_KEY = os.environ.get('SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('PUBLISHABLE_KEY')