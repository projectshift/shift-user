from flask import flash, redirect, render_template, url_for, abort, current_app
from flask import request
from flask.views import View
from flask_login import current_user

from shiftuser.forms import ChangeEmailForm, ChangePasswordForm
from shiftuser.models import UpdateSchema
from shiftuser.services import user_service

"""
User profile
This is a collection of user profile screens implemented as pluggable
class-based views that you can connect and re-wire in your concrete flask apps
"""


# -----------------------------------------------------------------------------
# Reusable components
# -----------------------------------------------------------------------------

def guest_access(func):
    """
    Guest access decorator
    Checks if public profiles option is enabled in config and checks
    access to profile pages based on that.
    """
    def decorated(*_, **kwargs):
        public_profiles = current_app.config['USER_PUBLIC_PROFILES']
        if not public_profiles:
            if not current_user.is_authenticated:
                abort(401)
            elif current_user.id != kwargs['id']:
                abort(403)
        return func(**kwargs)

    return decorated


def only_owner(func):
    """
    Only owner decorator
    Restricts access to view ony to profile owner
    """
    def decorated(*_, **kwargs):
        id = kwargs['id']
        if not current_user.is_authenticated:
            abort(401)
        elif current_user.id != id:
            abort(403)
        return func(**kwargs)

    return decorated


class Me(View):
    """ Me redirects to current user profile """
    profile_endpoint = 'user.profile.home'
    login_endpoint = 'user.login'

    def dispatch_request(self):
        if current_user.is_authenticated:
            return redirect(url_for(self.profile_endpoint, id=current_user.id))
        else:
            return redirect(url_for(self.login_endpoint))


class Profile(View):
    """ Generic profile view """
    decorators = [only_owner]
    flash = False  # flash messages

    def dispatch_request(self):
        raise NotImplementedError()

    def is_myself(self, id):
        if current_user.is_authenticated and id == current_user.id:
            return True
        return False

# -----------------------------------------------------------------------------
# Profile home
# -----------------------------------------------------------------------------


class ProfileHome(Profile):
    """ Displays user profile page """
    decorators = [guest_access]
    template = 'profile/home.j2'

    def dispatch_request(self, id=None):
        public_profiles = current_app.config['USER_PUBLIC_PROFILES']
        if not public_profiles:
            if not current_user.is_authenticated:
                abort(401)
            elif current_user.id != id:
                abort(403)

        user = user_service.get_or_404(id)
        myself = self.is_myself(id)
        return render_template(self.template, myself=myself, user=user)


# -----------------------------------------------------------------------------
# Email
# -----------------------------------------------------------------------------

class ProfileEmailChange(Profile):
    """ Email changer screen """
    template = 'profile/email.j2'
    form = ChangeEmailForm
    schema = UpdateSchema
    invalid_message = 'Form invalid'
    exception_message = 'Service error'
    ok_message = 'Email update confirmation sent. Please check inbox.'
    cancel_message = 'Request to change email was cancelled'
    flash = False

    def dispatch_request(self, id=None):
        user = user_service.get_or_404(id)
        myself = self.is_myself(id)
        form = self.form(schema=self.schema(), context=user)
        params = dict(form=form, user=user, myself=myself)

        # is this a request to cancel change?
        if myself and 'cancel_change' in request.args:
            user.cancel_email_change()
            user_service.save(user)
            if self.flash:
                flash(self.cancel_message)
            return render_template(self.template, **params)

        # otherwise change
        cfg = current_app.config
        base_confirm_url = cfg.get('USER_BASE_EMAIL_CONFIRM_URL')
        if not base_confirm_url:
            base_confirm_url = url_for(
                'user.confirm.email.request',
                _external=True
            )

        if form.validate_on_submit():
            ok = user_service.change_email(
                user=user,
                new_email=form.email.data,
                base_confirm_url=base_confirm_url
            )
            if ok:
                if self.flash:
                    flash(self.ok_message, 'success')
                return render_template(self.template, **params)
            else:
                if self.flash:
                    flash(self.exception_message, 'danger')
        elif form.is_submitted():
            if self.flash:
                flash(self.invalid_message, 'danger')

        return render_template(self.template, **params)

# -----------------------------------------------------------------------------
# Password
# -----------------------------------------------------------------------------


class ProfilePasswordChange(Profile):
    """ Password changer screen """
    template = 'profile/password.j2'
    form = ChangePasswordForm
    schema = UpdateSchema
    invalid_message = 'Form invalid'
    ok_message = 'Password changed. Please login.'
    ok_redirect = 'user.login'
    exception_message = 'Password change failed.'
    flash = False

    def dispatch_request(self, id=None):
        user = user_service.get_or_404(id)
        myself = self.is_myself(id)
        form = self.form(schema=self.schema(), context=user)
        if form.validate_on_submit():
            ok = user_service.change_password(user, form.password.data)
            if ok:
                if self.flash:
                    flash(self.ok_message, 'success')
                return redirect(url_for(self.ok_redirect))
            else:
                if self.flash:
                    flash(self.exception_message, 'danger')

        params = dict(form=form, user=user, myself=myself)
        return render_template(self.template, **params)
