from flask_login import LoginManager
from flask_principal import Principal

from shiftuser.role_service import RoleService
from shiftuser.user_service import UserService

# instantiate user services (bootstrapped later by user feature)
login_manager = LoginManager()
principal = Principal()
role_service = RoleService()
user_service = UserService()

