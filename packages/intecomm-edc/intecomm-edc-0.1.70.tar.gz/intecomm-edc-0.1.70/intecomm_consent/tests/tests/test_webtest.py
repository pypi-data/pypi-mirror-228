from unittest.mock import patch

import django
from django.conf import global_settings
from django.conf.locale import LANG_INFO
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse
from django_webtest import WebTest
from edc_dashboard import url_names

from intecomm_dashboard.views import SubjectDashboardView
from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin
from intecomm_subject.models import DrugSupplyDm, DrugSupplyHiv, DrugSupplyHtn
from intecomm_subject.models import HealthEconomics as OldHealthEconomics

EXTRA_LANG_INFO = {
    "mas": {
        "bidi": False,
        "code": "mas",
        "name": "Masaai",
        "name_local": "Masaai",
    },
    "ry": {
        "bidi": False,
        "code": "ry",
        "name": "Runyakitara",
        "name_local": "Runyakitara",
    },
    "rny": {
        "bidi": False,
        "code": "rny",
        "name": "Runyankore",
        "name_local": "Runyankore",
    },
    "lg": {
        "bidi": False,
        "code": "lg",
        "name": "Luganda",
        "name_local": "Luganda",
    },
}

django.conf.locale.LANG_INFO = LANG_INFO
# Add custom languages not provided by Django
LANG_INFO = dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO)
django.conf.locale.LANG_INFO = LANG_INFO


@override_settings(
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
    LANG_INFO=dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO),
    LANGUAGES_BIDI=global_settings.LANGUAGES_BIDI + ["mas", "ry", "lg", "rny"],
    LANGUAGE_CODE="en-gb",
)
class TestSubjectDashboard(IntecommTestCaseMixin, WebTest):
    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create_superuser("user_login", "u@example.com", "pass")
        self.user.is_active = True
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.user.refresh_from_db()
        self.exclude_models = [
            DrugSupplyDm,
            DrugSupplyHtn,
            DrugSupplyHiv,
            OldHealthEconomics,
        ]

    def login(self):
        form = None
        response = self.app.get(reverse("admin:index")).maybe_follow()
        for index, form in response.forms.items():
            if form.action == "/i18n/setlang/":
                # exclude the locale form
                continue
            else:
                break
        form["username"] = self.user.username
        form["password"] = "pass"  # nosec B105
        return form.submit()

    @patch("intecomm_dashboard.views.subject.dashboard.dashboard_view.get_current_country")
    def test_dashboard_ok(self, mock_get_current_country):
        mock_get_current_country.result = "uganda"
        subject_screening = self.get_subject_screening()
        self.assertEqual(subject_screening.reasons_ineligible, None)
        self.assertTrue(subject_screening.eligible)

        subject_consent = self.get_subject_consent(subject_screening)
        self.assertIsNotNone(subject_consent.subject_identifier)

        self.login()

        url_name = url_names.get(SubjectDashboardView.dashboard_url_name)
        url = reverse(
            url_name, kwargs=dict(subject_identifier=subject_consent.subject_identifier)
        )
        self.app.get(url, user=self.user, status=200)
