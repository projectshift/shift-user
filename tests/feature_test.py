from nose.plugins.attrib import attr
from tests.base_testcase import BaseTestCase

from boiler import bootstrap
from boiler.config import DefaultConfig
from shiftuser import exceptions as x
from shiftuser.services import user_service
from shiftuser.feature import user_feature
from shiftuser.config import UserConfig

@attr('feature', 'user')
class UserFeatureTests(BaseTestCase):

    # ------------------------------------------------------------------------
    # General
    # ------------------------------------------------------------------------

    def test_fail_to_init_feature_if_jwt_secret_not_set(self):
        """ Fail to initialize user feature without JWT secret"""
        config = DefaultConfig()
        config.USER_JWT_SECRET = None
        app = bootstrap.create_app(__name__, config=config)
        with self.assertRaises(x.JwtSecretMissing):
            user_feature(app)

    def test_user_service_receives_config_options(self):
        """ Initializing user service with config options """
        class CustomConfig(DefaultConfig, UserConfig):
            USER_JWT_SECRET = '123'
            USER_PUBLIC_PROFILES = False
            USER_ACCOUNTS_REQUIRE_CONFIRMATION = False
            USER_SEND_WELCOME_MESSAGE = False
            USER_EMAIL_SUBJECTS = {}
        app = bootstrap.create_app(__name__, config=CustomConfig())
        user_feature(app)

        self.assertEquals(
            CustomConfig.USER_PUBLIC_PROFILES,
            user_service.welcome_message
        )
        self.assertEquals(
            CustomConfig.USER_ACCOUNTS_REQUIRE_CONFIRMATION,
            user_service.require_confirmation
        )
        self.assertEquals(
            CustomConfig.USER_EMAIL_SUBJECTS,
            user_service.email_subjects
        )











