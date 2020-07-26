from datetime import datetime, timedelta, date
from django.utils import timezone

CURRENT_DATE = timezone.now
LATER90D = datetime.date(datetime.today()) + timedelta(days=90)
LATER30D = datetime.date(datetime.today()) + timedelta(days=30)