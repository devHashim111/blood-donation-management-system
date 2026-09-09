
from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from .models import BloodRequest, Contact, News, ReadyDonors


class NewsModelTests(TestCase):
    def test_create_news(self):
        news = News.objects.create(
            title="Blood Donation Awareness Camp",
            detail="<p>A blood donation camp will be held this Sunday.</p>",
        )

        self.assertIsNotNone(news.pk)
        self.assertEqual(news.title, "Blood Donation Awareness Camp")
        self.assertEqual(
            news.detail,
            "<p>A blood donation camp will be held this Sunday.</p>",
        )

    def test_news_can_store_html_content(self):
        detail = (
            "<h2>Emergency Blood Camp</h2>"
            "<p><strong>O- blood</strong> is urgently required.</p>"
        )

        news = News.objects.create(
            title="Emergency Blood Camp",
            detail=detail,
        )

        news.refresh_from_db()

        self.assertEqual(news.detail, detail)
        self.assertIn("<h2>", news.detail)
        self.assertIn("<strong>O- blood</strong>", news.detail)

    def test_news_title_max_length(self):
        news = News(
            title="x" * 101,
            detail="<p>Test</p>",
        )

        with self.assertRaises(ValidationError):
            news.full_clean()

    def test_news_title_at_max_length_is_valid(self):
        news = News(
            title="x" * 100,
            detail="<p>Test</p>",
        )

        news.full_clean()

    def test_news_persists_after_refresh(self):
        news = News.objects.create(
            title="Donation Drive",
            detail="<p>Community blood donation drive.</p>",
        )

        pk = news.pk
        news.refresh_from_db()

        self.assertEqual(news.pk, pk)
        self.assertEqual(news.title, "Donation Drive")

    def test_news_pk_is_unique_within_model(self):
        first = News.objects.create(
            title="First",
            detail="<p>First article</p>",
        )
        second = News.objects.create(
            title="Second",
            detail="<p>Second article</p>",
        )

        self.assertNotEqual(first.pk, second.pk)


class ContactModelTests(TestCase):
    def test_create_contact(self):
        contact = Contact.objects.create(
            name="Ali Khan",
            email="ali@example.com",
            message="I want to volunteer as a blood donor.",
        )

        self.assertIsNotNone(contact.pk)
        self.assertEqual(contact.name, "Ali Khan")
        self.assertEqual(contact.email, "ali@example.com")
        self.assertEqual(
            contact.message,
            "I want to volunteer as a blood donor.",
        )

    def test_contact_email_validation(self):
        contact = Contact(
            name="Ali",
            email="invalid-email",
            message="Test",
        )

        with self.assertRaises(ValidationError):
            contact.full_clean()

    def test_contact_name_max_length(self):
        contact = Contact(
            name="x" * 51,
            email="ali@example.com",
            message="Test",
        )

        with self.assertRaises(ValidationError):
            contact.full_clean()

    def test_contact_name_at_max_length_is_valid(self):
        contact = Contact(
            name="x" * 50,
            email="ali@example.com",
            message="Test",
        )

        contact.full_clean()

    def test_contact_message_accepts_null(self):
        contact = Contact.objects.create(
            name="Ali",
            email="ali@example.com",
            message=None,
        )

        contact.refresh_from_db()

        self.assertIsNone(contact.message)

    def test_contact_message_accepts_empty_string(self):
        contact = Contact.objects.create(
            name="Ali",
            email="ali@example.com",
            message="",
        )

        contact.refresh_from_db()

        self.assertEqual(contact.message, "")

    def test_contact_email_at_maximum_normal_length(self):
        contact = Contact(
            name="Ali",
            email="a" * 50 + "@example.com",
            message="Test",
        )

        contact.full_clean()


class BloodRequestModelTests(TestCase):
    BLOOD_GROUPS = {
        "A+",
        "A-",
        "B+",
        "B-",
        "O+",
        "O-",
        "AB+",
        "AB-",
    }

    def valid_data(self, **overrides):
        data = {
            "blood_group": "O+",
            "location": "Lahore",
            "disease": "Emergency Surgery",
            "time_limit": timezone.now() + timedelta(days=1),
            "hospital": "City Hospital",
            "attendant_name": "Ahmed Khan",
            "contact": "03001234567",
            "pick_drop_service": False,
            "is_solved": False,
        }
        data.update(overrides)
        return data

    def test_create_blood_request(self):
        request = BloodRequest.objects.create(
            **self.valid_data()
        )

        self.assertIsNotNone(request.pk)
        self.assertEqual(request.blood_group, "O+")
        self.assertEqual(request.location, "Lahore")
        self.assertEqual(request.disease, "Emergency Surgery")
        self.assertEqual(request.hospital, "City Hospital")
        self.assertEqual(request.attendant_name, "Ahmed Khan")
        self.assertEqual(request.contact, "03001234567")
        self.assertFalse(request.pick_drop_service)
        self.assertFalse(request.is_solved)

    def test_blood_request_string_representation(self):
        request = BloodRequest.objects.create(
            **self.valid_data(
                blood_group="A-",
                hospital="General Hospital",
            )
        )

        self.assertEqual(
            str(request),
            "A- needed at General Hospital",
        )

    def test_blood_request_created_at_is_automatically_populated(self):
        before = timezone.now()

        request = BloodRequest.objects.create(
            **self.valid_data()
        )

        after = timezone.now()

        self.assertIsNotNone(request.created_at)
        self.assertGreaterEqual(request.created_at, before)
        self.assertLessEqual(request.created_at, after)

    def test_blood_request_created_at_is_timezone_aware(self):
        request = BloodRequest.objects.create(
            **self.valid_data()
        )

        self.assertTrue(
            timezone.is_aware(request.created_at)
        )

    def test_pick_drop_defaults_to_false(self):
        request = BloodRequest.objects.create(
            **self.valid_data()
        )

        self.assertFalse(request.pick_drop_service)

    def test_is_solved_defaults_to_false(self):
        request = BloodRequest.objects.create(
            **self.valid_data()
        )

        self.assertFalse(request.is_solved)

    def test_pick_drop_service_can_be_enabled(self):
        request = BloodRequest.objects.create(
            **self.valid_data(
                pick_drop_service=True,
            )
        )

        self.assertTrue(request.pick_drop_service)

    def test_request_can_be_marked_solved(self):
        request = BloodRequest.objects.create(
            **self.valid_data()
        )

        request.is_solved = True
        request.save(update_fields=["is_solved"])
        request.refresh_from_db()

        self.assertTrue(request.is_solved)

    def test_all_blood_groups_are_defined(self):
        field = BloodRequest._meta.get_field("blood_group")

        actual = {
            value
            for value, _label in field.choices
        }

        self.assertEqual(actual, self.BLOOD_GROUPS)

    def test_valid_blood_groups_pass_validation(self):
        for blood_group in self.BLOOD_GROUPS:
            request = BloodRequest(
                **self.valid_data(
                    blood_group=blood_group,
                )
            )

            try:
                request.full_clean()
            except ValidationError as exc:
                self.fail(
                    f"Blood group {blood_group} unexpectedly failed: {exc}"
                )

    def test_invalid_blood_group_fails_validation(self):
        request = BloodRequest(
            **self.valid_data(
                blood_group="X+",
            )
        )

        with self.assertRaises(ValidationError):
            request.full_clean()

    def test_missing_required_fields_fail_validation(self):
        request = BloodRequest()

        with self.assertRaises(ValidationError):
            request.full_clean()

    def test_time_limit_accepts_future_datetime(self):
        time_limit = timezone.now() + timedelta(hours=6)

        request = BloodRequest(
            **self.valid_data(
                time_limit=time_limit,
            )
        )

        request.full_clean()

    def test_request_can_be_saved_with_past_time_limit(self):
        time_limit = timezone.now() - timedelta(hours=1)

        request = BloodRequest.objects.create(
            **self.valid_data(
                time_limit=time_limit,
            )
        )

        self.assertEqual(
            request.time_limit,
            time_limit,
        )

    def test_unsolved_requests_can_be_filtered(self):
        BloodRequest.objects.create(
            **self.valid_data(
                is_solved=False,
                hospital="Open Hospital",
            )
        )
        BloodRequest.objects.create(
            **self.valid_data(
                is_solved=True,
                hospital="Closed Hospital",
            )
        )

        requests = BloodRequest.objects.filter(
            is_solved=False
        )

        self.assertEqual(requests.count(), 1)
        self.assertEqual(
            requests.get().hospital,
            "Open Hospital",
        )

    def test_requests_can_be_filtered_by_blood_group(self):
        BloodRequest.objects.create(
            **self.valid_data(
                blood_group="O+",
            )
        )
        BloodRequest.objects.create(
            **self.valid_data(
                blood_group="A+",
            )
        )
        BloodRequest.objects.create(
            **self.valid_data(
                blood_group="O+",
            )
        )

        requests = BloodRequest.objects.filter(
            blood_group="O+"
        )

        self.assertEqual(requests.count(), 2)

    def test_requests_can_be_filtered_by_hospital(self):
        BloodRequest.objects.create(
            **self.valid_data(
                hospital="Mayo Hospital",
            )
        )
        BloodRequest.objects.create(
            **self.valid_data(
                hospital="General Hospital",
            )
        )

        requests = BloodRequest.objects.filter(
            hospital="Mayo Hospital"
        )

        self.assertEqual(requests.count(), 1)

    def test_expired_requests_can_be_identified(self):
        now = timezone.now()

        expired = BloodRequest.objects.create(
            **self.valid_data(
                time_limit=now - timedelta(hours=2),
                hospital="Expired Hospital",
            )
        )

        active = BloodRequest.objects.create(
            **self.valid_data(
                time_limit=now + timedelta(hours=2),
                hospital="Active Hospital",
            )
        )

        expired_requests = BloodRequest.objects.filter(
            time_limit__lt=now
        )

        self.assertIn(expired.pk, expired_requests.values_list("pk", flat=True))
        self.assertNotIn(active.pk, expired_requests.values_list("pk", flat=True))


class ReadyDonorModelTests(TestCase):
    BLOOD_GROUPS = {
        "A+",
        "A-",
        "B+",
        "B-",
        "O+",
        "O-",
        "AB+",
        "AB-",
    }

    GENDERS = {
        "Male",
        "Female",
        "Other",
    }

    DONATION_TIMES = {
        "Urgent",
        "Blood Bank",
    }

    def valid_data(self, **overrides):
        data = {
            "name": "Muhammad Ali",
            "address": "Model Town, Lahore",
            "age": 28,
            "gender": "Male",
            "weight": 72.5,
            "disease": None,
            "blood_group": "O+",
            "phone": "03001234567",
            "email": "ali@example.com",
            "donation_time": "Urgent",
        }
        data.update(overrides)
        return data

    def test_create_ready_donor(self):
        donor = ReadyDonors.objects.create(
            **self.valid_data()
        )

        self.assertIsNotNone(donor.pk)
        self.assertEqual(donor.name, "Muhammad Ali")
        self.assertEqual(donor.address, "Model Town, Lahore")
        self.assertEqual(donor.age, 28)
        self.assertEqual(donor.gender, "Male")
        self.assertEqual(
            donor.weight,
            Decimal("72.5"),
        ) if isinstance(donor.weight, Decimal) else self.assertEqual(
            donor.weight,
            72.5,
        )
        self.assertEqual(donor.blood_group, "O+")
        self.assertEqual(donor.phone, "03001234567")
        self.assertEqual(donor.email, "ali@example.com")
        self.assertEqual(
            donor.donation_time,
            "Urgent",
        )

    def test_ready_donor_string_representation(self):
        donor = ReadyDonors.objects.create(
            **self.valid_data(
                name="Hamza",
                blood_group="A+",
            )
        )

        self.assertEqual(
            str(donor),
            "Hamza (A+)",
        )

    def test_ready_donor_string_without_blood_group(self):
        donor = ReadyDonors.objects.create(
            **self.valid_data(
                name="Usman",
                blood_group=None,
            )
        )

        self.assertEqual(
            str(donor),
            "Usman (No Blood Group)",
        )

    def test_blood_group_is_optional(self):
        donor = ReadyDonors.objects.create(
            **self.valid_data(
                blood_group=None,
            )
        )

        self.assertIsNone(donor.blood_group)

    def test_disease_is_optional(self):
        donor = ReadyDonors.objects.create(
            **self.valid_data(
                disease=None,
            )
        )

        self.assertIsNone(donor.disease)

    def test_address_is_optional(self):
        donor = ReadyDonors.objects.create(
            **self.valid_data(
                address=None,
            )
        )

        self.assertIsNone(donor.address)

    def test_email_is_optional(self):
        donor = ReadyDonors.objects.create(
            **self.valid_data(
                email=None,
            )
        )

        self.assertIsNone(donor.email)

    def test_donation_time_is_optional(self):
        donor = ReadyDonors.objects.create(
            **self.valid_data(
                donation_time=None,
            )
        )

        self.assertIsNone(donor.donation_time)

    def test_created_at_is_automatic(self):
        before = timezone.now()

        donor = ReadyDonors.objects.create(
            **self.valid_data()
        )

        after = timezone.now()

        self.assertIsNotNone(donor.created_at)
        self.assertGreaterEqual(donor.created_at, before)
        self.assertLessEqual(donor.created_at, after)

    def test_created_at_is_timezone_aware(self):
        donor = ReadyDonors.objects.create(
            **self.valid_data()
        )

        self.assertTrue(
            timezone.is_aware(donor.created_at)
        )

    def test_created_at_does_not_change_after_update(self):
        donor = ReadyDonors.objects.create(
            **self.valid_data()
        )

        original_created_at = donor.created_at

        donor.name = "Updated Donor"
        donor.save()
        donor.refresh_from_db()

        self.assertEqual(
            donor.created_at,
            original_created_at,
        )

    def test_gender_choices(self):
        field = ReadyDonors._meta.get_field("gender")

        actual = {
            value
            for value, _label in field.choices
        }

        self.assertEqual(actual, self.GENDERS)

    def test_blood_group_choices(self):
        field = ReadyDonors._meta.get_field("blood_group")

        actual = {
            value
            for value, _label in field.choices
        }

        self.assertEqual(actual, self.BLOOD_GROUPS)

    def test_donation_time_choices(self):
        field = ReadyDonors._meta.get_field("donation_time")

        actual = {
            value
            for value, _label in field.choices
        }

        self.assertEqual(
            actual,
            self.DONATION_TIMES,
        )

    def test_valid_genders_pass_validation(self):
        for gender in self.GENDERS:
            donor = ReadyDonors(
                **self.valid_data(
                    gender=gender,
                )
            )

            try:
                donor.full_clean()
            except ValidationError as exc:
                self.fail(
                    f"Gender {gender} unexpectedly failed: {exc}"
                )

    def test_invalid_gender_fails_validation(self):
        donor = ReadyDonors(
            **self.valid_data(
                gender="Unknown",
            )
        )

        with self.assertRaises(ValidationError):
            donor.full_clean()

    def test_invalid_blood_group_fails_validation(self):
        donor = ReadyDonors(
            **self.valid_data(
                blood_group="X+",
            )
        )

        with self.assertRaises(ValidationError):
            donor.full_clean()

    def test_invalid_donation_time_fails_validation(self):
        donor = ReadyDonors(
            **self.valid_data(
                donation_time="Tomorrow",
            )
        )

        with self.assertRaises(ValidationError):
            donor.full_clean()

    def test_negative_age_fails_validation(self):
        donor = ReadyDonors(
            **self.valid_data(
                age=-1,
            )
        )

        with self.assertRaises(ValidationError):
            donor.full_clean()

    def test_zero_age_is_valid_for_model_field(self):
        donor = ReadyDonors(
            **self.valid_data(
                age=0,
            )
        )

        donor.full_clean()

    def test_zero_weight_is_valid_for_model_field(self):
        donor = ReadyDonors(
            **self.valid_data(
                weight=0,
            )
        )

        donor.full_clean()

    def test_required_phone_fails_validation_when_missing(self):
        donor = ReadyDonors(
            **self.valid_data(
                phone="",
            )
        )

        with self.assertRaises(ValidationError):
            donor.full_clean()

    def test_invalid_email_fails_validation(self):
        donor = ReadyDonors(
            **self.valid_data(
                email="invalid-email",
            )
        )

        with self.assertRaises(ValidationError):
            donor.full_clean()

    def test_donor_can_be_marked_for_blood_bank(self):
        donor = ReadyDonors.objects.create(
            **self.valid_data(
                donation_time="Blood Bank",
            )
        )

        self.assertEqual(
            donor.donation_time,
            "Blood Bank",
        )

    def test_donors_can_be_filtered_by_blood_group(self):
        ReadyDonors.objects.create(
            **self.valid_data(
                name="O Positive One",
                blood_group="O+",
            )
        )
        ReadyDonors.objects.create(
            **self.valid_data(
                name="O Positive Two",
                blood_group="O+",
            )
        )
        ReadyDonors.objects.create(
            **self.valid_data(
                name="A Positive",
                blood_group="A+",
            )
        )

        donors = ReadyDonors.objects.filter(
            blood_group="O+"
        )

        self.assertEqual(donors.count(), 2)

    def test_donors_without_blood_group_can_be_found(self):
        ReadyDonors.objects.create(
            **self.valid_data(
                name="Known Group",
                blood_group="A+",
            )
        )
        ReadyDonors.objects.create(
            **self.valid_data(
                name="Unknown Group",
                blood_group=None,
            )
        )

        donors = ReadyDonors.objects.filter(
            blood_group__isnull=True
        )

        self.assertEqual(donors.count(), 1)
        self.assertEqual(
            donors.get().name,
            "Unknown Group",
        )

    def test_donor_update_persists(self):
        donor = ReadyDonors.objects.create(
            **self.valid_data()
        )

        donor.name = "Updated Name"
        donor.phone = "03221234567"
        donor.save()

        donor.refresh_from_db()

        self.assertEqual(
            donor.name,
            "Updated Name",
        )
        self.assertEqual(
            donor.phone,
            "03221234567",
        )


class BloodDonationWorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request = BloodRequest.objects.create(
            blood_group="O+",
            location="Lahore",
            disease="Emergency Surgery",
            time_limit=timezone.now() + timedelta(hours=12),
            hospital="General Hospital",
            attendant_name="Ahmed Khan",
            contact="03001234567",
            pick_drop_service=True,
            is_solved=False,
        )

        cls.matching_donor = ReadyDonors.objects.create(
            name="Ali Raza",
            address="Johar Town, Lahore",
            age=30,
            gender="Male",
            weight=75.0,
            disease=None,
            blood_group="O+",
            phone="03111234567",
            email="ali@example.com",
            donation_time="Urgent",
        )

        cls.non_matching_donor = ReadyDonors.objects.create(
            name="Usman Khan",
            address="DHA, Lahore",
            age=27,
            gender="Male",
            weight=70.0,
            disease=None,
            blood_group="A+",
            phone="03221234567",
            email="usman@example.com",
            donation_time="Urgent",
        )

    def test_matching_donor_can_be_found_for_request(self):
        donors = ReadyDonors.objects.filter(
            blood_group=self.request.blood_group
        )

        self.assertIn(
            self.matching_donor.pk,
            donors.values_list("pk", flat=True),
        )

        self.assertNotIn(
            self.non_matching_donor.pk,
            donors.values_list("pk", flat=True),
        )

    def test_urgent_matching_donor_can_be_selected(self):
        donors = ReadyDonors.objects.filter(
            blood_group=self.request.blood_group,
            donation_time="Urgent",
        )

        self.assertEqual(donors.count(), 1)
        self.assertEqual(
            donors.get().pk,
            self.matching_donor.pk,
        )

    def test_request_can_be_marked_solved(self):
        self.assertFalse(self.request.is_solved)

        self.request.is_solved = True
        self.request.save(update_fields=["is_solved"])
        self.request.refresh_from_db()

        self.assertTrue(self.request.is_solved)

    def test_unsolved_matching_requests_can_be_found(self):
        requests = BloodRequest.objects.filter(
            blood_group=self.matching_donor.blood_group,
            is_solved=False,
        )

        self.assertEqual(requests.count(), 1)
        self.assertEqual(
            requests.get().pk,
            self.request.pk,
        )

    def test_request_and_donor_are_independent_records(self):
        self.assertIsInstance(
            self.request,
            BloodRequest,
        )
        self.assertIsInstance(
            self.matching_donor,
            ReadyDonors,
        )

        self.assertEqual(
            BloodRequest.objects.count(),
            1,
        )
        self.assertEqual(
            ReadyDonors.objects.count(),
            2,
        )

        self.assertTrue(
            BloodRequest.objects.filter(
                pk=self.request.pk
            ).exists()
        )

        self.assertTrue(
            ReadyDonors.objects.filter(
                pk=self.matching_donor.pk
            ).exists()
        )

    def test_primary_keys_are_only_unique_per_model(self):
        self.assertEqual(
            BloodRequest.objects.filter(
                pk=self.request.pk
            ).count(),
            1,
        )

        self.assertEqual(
            ReadyDonors.objects.filter(
                pk=self.request.pk
            ).count(),
            1,
        )

    def test_solved_request_is_excluded_from_open_requests(self):
        self.request.is_solved = True
        self.request.save(update_fields=["is_solved"])

        open_requests = BloodRequest.objects.filter(
            blood_group="O+",
            is_solved=False,
        )

        self.assertEqual(open_requests.count(), 0)

    def test_donor_with_different_blood_group_is_not_a_match(self):
        matching = ReadyDonors.objects.filter(
            blood_group=self.request.blood_group
        )

        self.assertEqual(
            matching.filter(
                pk=self.non_matching_donor.pk
            ).count(),
            0,
        )

    def test_request_and_donor_records_can_be_retrieved_independently(self):
        request = BloodRequest.objects.get(
            pk=self.request.pk
        )
        donor = ReadyDonors.objects.get(
            pk=self.matching_donor.pk
        )

        self.assertEqual(
            request.hospital,
            "General Hospital",
        )
        self.assertEqual(
            donor.name,
            "Ali Raza",
        )

    def test_multiple_requests_can_share_same_blood_group(self):
        second_request = BloodRequest.objects.create(
            blood_group="O+",
            location="Islamabad",
            disease="Accident",
            time_limit=timezone.now() + timedelta(hours=5),
            hospital="Capital Hospital",
            attendant_name="Hassan",
            contact="03331234567",
            pick_drop_service=False,
            is_solved=False,
        )

        requests = BloodRequest.objects.filter(
            blood_group="O+",
            is_solved=False,
        )

        self.assertEqual(requests.count(), 2)
        self.assertIn(
            second_request.pk,
            requests.values_list("pk", flat=True),
        )

