import string
from datetime import timedelta, datetime

# for robot validation
MODEL_LEN = 2
VERSION_LEN = 2
LETTERS = string.ascii_letters + string.digits
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# for robot summary
PERIOD = datetime.today() - timedelta(days=7)

# for client validation
EMAIL_LEN = 255

# for order validation
SERIAL_LEN = 5
