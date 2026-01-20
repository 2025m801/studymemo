from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Memo

class MemoSmokeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u1", password="pass12345")
        self.client.login(username="u1", password="pass12345")
        self.memo = Memo.objects.create(user=self.user, title="t", content="c")

    def test_list_page_ok(self):
        res = self.client.get(reverse("memo_list"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "メモ")

    def test_favorite_toggle(self):
        url = reverse("memo_favorite_toggle", args=[self.memo.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, 200)
        self.memo.refresh_from_db()
        self.assertTrue(self.memo.is_favorite)
