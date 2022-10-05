from django.test import TestCase
from django.urls import reverse
from .views import *


class Test_login_logout(TestCase):
    def test_login_fail(self):
        response=self.client.get(reverse(home), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=%2F')
        response=self.client.get(reverse(add_patient), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=%2Fadd%2F')
        response=self.client.get(reverse(display_patient), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=%2Fdisplay%2F')
        response=self.client.get(reverse(update_patient_details, args=[1]), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=%2Fdisplay%2Fupdate%2F1')
        response=self.client.get(reverse(send_patient_email, args=[1]), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=%2Fmail%2F1%2F')
