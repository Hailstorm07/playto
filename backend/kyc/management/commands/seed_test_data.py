from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from rest_framework.authtoken.models import Token

from kyc.models import KYCSubmission, User


TEST_PASSWORD = 'password123'


class Command(BaseCommand):
    help = 'Create idempotent demo users and KYC submissions.'

    def handle(self, *args, **options):
        reviewer = self.ensure_user(
            username='reviewer1',
            email='reviewer@playto.com',
            role='reviewer',
        )
        reviewer2 = self.ensure_user(
            username='reviewer2',
            email='reviewer2@playto.com',
            role='reviewer',
        )

        merchant_draft = self.ensure_user(
            username='merchant_draft',
            email='m1@playto.com',
            role='merchant',
        )
        self.ensure_submission(
            merchant=merchant_draft,
            status='draft',
            full_name='John Draft',
            business_name='Draft Ventures',
        )

        merchant_review = self.ensure_user(
            username='merchant_review',
            email='m2@playto.com',
            role='merchant',
        )
        self.ensure_submission(
            merchant=merchant_review,
            assigned_reviewer=reviewer,
            status='under_review',
            full_name='Alice Review',
            email='alice@review.com',
            phone='+91 98765 43210',
            business_name='Review Corp',
            business_type='proprietorship',
            expected_monthly_volume=5000,
            last_status_change_at=timezone.now() - timedelta(hours=25),
        )

        merchant_submitted = self.ensure_user(
            username='merchant_submitted',
            email='m3@playto.com',
            role='merchant',
        )
        self.ensure_submission(
            merchant=merchant_submitted,
            assigned_reviewer=reviewer2,
            status='submitted',
            full_name='Bob Sub',
            email='m3@playto.com',
            phone='+91 99999 88888',
            business_name='Sub Systems',
            business_type='individual',
            expected_monthly_volume=2000,
            last_status_change_at=timezone.now() - timedelta(hours=10),
        )

        self.stdout.write(self.style.SUCCESS('Test data is ready.'))

    def ensure_user(self, username, email, role):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'role': role,
            },
        )
        updated = False
        if user.email != email:
            user.email = email
            updated = True
        if user.role != role:
            user.role = role
            updated = True
        if created or not user.has_usable_password():
            user.set_password(TEST_PASSWORD)
            updated = True
        if updated:
            user.save()

        Token.objects.get_or_create(user=user)
        action = 'created' if created else 'verified'
        self.stdout.write(f'{action}: {username} / {TEST_PASSWORD}')
        return user

    def ensure_submission(self, merchant, **defaults):
        submission, created = KYCSubmission.objects.update_or_create(
            merchant=merchant,
            defaults=defaults,
        )
        action = 'created' if created else 'updated'
        self.stdout.write(f'{action}: {merchant.username} submission ({submission.status})')
        return submission
