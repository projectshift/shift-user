from boiler import bootstrap
from boiler.config import TestingConfig
from shiftuser.feature import users_feature

"""
Create app for testing
This is not a real application, we only use it to run tests against.
"""


class Config(TestingConfig):
    USER_JWT_SECRET = 'typically will come from environment'
    SECRET_KEY = 'supersecret'


# create app
app = bootstrap.create_app(__name__, config=Config(),)
bootstrap.add_orm(app)
bootstrap.add_mail(app)
bootstrap.add_routing(app)



