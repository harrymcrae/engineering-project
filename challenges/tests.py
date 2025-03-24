from django.test import TestCase
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Challenge, Quiz, Bonus
from accounts.models import UserProfile

class ChallengeTests(TestCase):
    def setUp(self):
        # Create test user, user profile, and sample data
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.profile = UserProfile.objects.create(user=self.user, points=0)
        
        self.challenge = Challenge.objects.create(
            challenge_name="Test Challenge",
            challenge_id="test-challenge",
            challenge_description="A sample challenge",
            latitude=51.5074,
            longitude=-0.1278,
            points_awarded=10
        )

        self.quiz = Quiz.objects.create(
            quiz_id="test-quiz",
            quiz_name="Test Quiz",
            points_awarded=5
        )

        self.bonus = Bonus.objects.create(
            bonus_id="daily-bonus",
            points_awarded=10
        )

        self.client = Client()

    def test_challenges_page_access(self):
        # Ensure the challenges page is accessible to logged-in users
        self.client.login(username="testuser", password="password123")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "challenges.html")

    def test_claim_registration_bonus(self):
        # Test that users can successfully claim the registration bonus
        self.client.login(username="testuser", password="password123")
        response = self.client.post("/claim-registration-bonus/")
        self.profile.refresh_from_db()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.profile.registration_bonus_claimed)
        self.assertEqual(self.profile.points, self.bonus.points_awarded)

    def test_claim_daily_bonus(self):
        # Test daily bonus claiming functionality
        self.client.login(username="testuser", password="password123")
        response = self.client.post("/claim-daily-bonus/")
        self.profile.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(self.profile.daily_bonus_time_claimed)
        self.assertEqual(self.profile.points, self.bonus.points_awarded)

    def test_quiz_reward(self):
        # Test rewarding points when a user completes a quiz
        self.client.login(username="testuser", password="password123")
        response = self.client.post(f"/quiz-reward/{self.quiz.quiz_id}/")
        self.profile.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.quiz, self.profile.quizzes_completed.all())
        self.assertEqual(self.profile.points, self.quiz.points_awarded)

    def test_challenge_reward(self):
        # Test rewarding points when a user completes a challenge
        self.client.login(username="testuser", password="password123")
        response = self.client.post(f"/challenge-reward/{self.challenge.challenge_id}/")
        self.profile.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.challenge, self.profile.challenges_completed.all())
        self.assertEqual(self.profile.points, self.challenge.points_awarded)

    def test_check_registration_bonus_claimed(self):
        # Test if registration bonus check API works correctly
        self.client.login(username="testuser", password="password123")
        response = self.client.get("/check-registration-bonus/")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("registration_bonus_claimed", response.json())

    def test_check_challenge_completed(self):
        # Test if checking completed challenges returns correct data
        self.client.login(username="testuser", password="password123")
        response = self.client.get(f"/check-challenge-completed/{self.challenge.challenge_id}/")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("challenge_completed", response.json())

    def test_check_quiz_completed(self):
        # Test if checking completed quizzes returns correct data
        self.client.login(username="testuser", password="password123")
        response = self.client.get(f"/check-quiz-completed/{self.quiz.quiz_id}/")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("quiz_completed", response.json())
>>>>>>> ff6e04a (Added tests for dashboard and achievement reward)
