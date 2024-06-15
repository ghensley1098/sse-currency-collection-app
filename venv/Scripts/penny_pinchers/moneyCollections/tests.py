import datetime

from django.test import TestCase
from django.utils import timezone
from .models import mCollection

class CollectionModelTests(TestCase):
    def test_was_published_recently_with_future_collection(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_collection = mCollection(pub_date=time)
        self.assertIs(future_collection.was_published_recently(), False)

