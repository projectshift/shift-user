from boiler.testing.testcase import ViewTestCase
from tests.test_app.app import app as test_app


class BaseTestCase(ViewTestCase):
    """
    Base test case
    Uses test case from shiftboiler to provide flask-integrated testing
    facilities.
    """
    def setUp(self, app=None):
        if not app:
            app = test_app
        super().setUp(app)

