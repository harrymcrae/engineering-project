from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from dashboard.models import Achievement
from badges.models import Badge
from dashboard.views import achievement_reward

class DashboardTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(  # Set up test user
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")  # Log in test user

        # Create a test badge
        self.badge = Badge.objects.create(
            name="Test Badge",  # Badge name
            description="Awarded for testing",  # Badge description
        )

        # Create a test achievement
        self.achievement = Achievement.objects.create(
            achievement_name="Test Achievement",  # Achievement name
            achievement_description="This is a test achievement",  # Achievement description
            achievement_id="A100",  # Achievement ID
            points_awarded=50,  # Points awarded
            threshold=5,  # Threshold for achievement
            achievement_type="challenge",  # Achievement type
            badge_awarded=self.badge,  # Badge awarded
        )

    def test_dashboard_page_loads(self):
        response = self.client.get(reverse("dashboard"))  # Test if dashboard page loads
        self.assertEqual(response.status_code, 200)  # Status should be 200
        self.assertTemplateUsed(response, "dashboard.html")  # Should use correct template
        self.assertContains(response, "Test Achievement")  # Should display test achievement

    def test_check_achievement_completed(self):
        response = self.client.get(reverse("check_achievement_completed", args=[self.achievement.id]))  # Test if achievement completion check works
        self.assertEqual(response.status_code, 200)  # Status should be 200
        self.assertIn("completed_achievements", response.json())  # Should return completed achievements in JSON response

    def test_claim_achievement_reward(self):
        response = self.client.post(reverse("achievement_reward", args=[self.achievement.id]))  # Test claiming achievement reward
        self.assertEqual(response.status_code, 200)  # Status should be 200
        self.assertIn("success", response.json())  # Response should indicate success

>>>>>>> ff6e04a (Added tests for dashboard and achievement reward)
