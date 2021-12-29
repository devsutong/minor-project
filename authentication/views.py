<<<<<<< HEAD
from allauth.account import views
from allauth.account import urls

# from django.contrib import messages
# from django.urls import reverse, reverse_lazy
# from allauth.utils import get_form_class
# from allauth.account import app_settings, signals
# from django.shortcuts import redirect
# from allauth.account.adapter import get_adapter

# from allauth.account.utils import (
#     perform_login,
# )

# from django.http import (
#     Http404,
#     HttpResponsePermanentRedirect,
#     HttpResponseRedirect,
# )

# from allauth.account.forms import (
#     UserTokenForm,
# )


# INTERNAL_RESET_URL_KEY = "set-password"
# INTERNAL_RESET_SESSION_KEY = "_password_reset_key"


# def _ajax_response(request, response, form=None, data=None):
#     adapter = get_adapter(request)
#     if adapter.is_ajax(request):
#         if isinstance(response, HttpResponseRedirect) or isinstance(
#             response, HttpResponsePermanentRedirect
#         ):
#             redirect_to = response["Location"]
#         else:
#             redirect_to = None
#         response = adapter.ajax_response(
#             request, response, form=form, data=data, redirect_to=redirect_to
#         )
#     return response



# class PasswordResetFromKeyView(views.PasswordResetFromKeyView):
#     template_name = "account/password_reset_from_key." + app_settings.TEMPLATE_EXTENSION
#     form_class = views.ResetPasswordKeyForm
#     success_url = reverse_lazy("account_reset_password_from_key_done")

#     def get_form_class(self):
#         return get_form_class(
#             app_settings.FORMS, "reset_password_from_key", self.form_class
#         )

#     def dispatch(self, request, uidb36, key, **kwargs):
#         self.request = request
#         self.key = key

#         if self.key == INTERNAL_RESET_URL_KEY:
#             self.key = self.request.session.get(INTERNAL_RESET_SESSION_KEY, "")
#             # (Ab)using forms here to be able to handle errors in XHR #890
#             token_form = UserTokenForm(data={"uidb36": uidb36, "key": self.key})
#             if token_form.is_valid():
#                 self.reset_user = token_form.reset_user

#                 # In the event someone clicks on a password reset link
#                 # for one account while logged into another account,
#                 # logout of the currently logged in account.
#                 if (
#                     self.request.user.is_authenticated
#                     and self.request.user.pk != self.reset_user.pk
#                 ):
#                     self.logout()
#                     self.request.session[INTERNAL_RESET_SESSION_KEY] = self.key

#                 return super(PasswordResetFromKeyView, self).dispatch(
#                     request, uidb36, self.key, **kwargs
#                 )
#         else:
#             token_form = UserTokenForm(data={"uidb36": uidb36, "key": self.key})
#             if token_form.is_valid():
#                 # Store the key in the session and redirect to the
#                 # password reset form at a URL without the key. That
#                 # avoids the possibility of leaking the key in the
#                 # HTTP Referer header.
#                 self.request.session[INTERNAL_RESET_SESSION_KEY] = self.key
#                 redirect_url = self.request.path.replace(
#                     self.key, INTERNAL_RESET_URL_KEY
#                 )
#                 return redirect(redirect_url)

#         self.reset_user = None
#         response = self.render_to_response(self.get_context_data(token_fail=True))
#         return _ajax_response(self.request, response, form=token_form)

#     def get_context_data(self, **kwargs):
#         ret = super(PasswordResetFromKeyView, self).get_context_data(**kwargs)
#         ret["action_url"] = reverse(
#             "account_reset_password_from_key",
#             kwargs={
#                 "uidb36": self.kwargs["uidb36"],
#                 "key": self.kwargs["key"],
#             },
#         )
#         return ret

#     def get_form_kwargs(self):
#         kwargs = super(PasswordResetFromKeyView, self).get_form_kwargs()
#         kwargs["user"] = self.reset_user
#         kwargs["temp_key"] = self.key
#         return kwargs

#     def form_valid(self, form):
#         form.save()
#         adapter = get_adapter(self.request)

#         if self.reset_user and app_settings.LOGIN_ATTEMPTS_LIMIT:
#             # User successfully reset the password, clear any
#             # possible cache entries for all email addresses.
#             for email in self.reset_user.emailaddress_set.all():
#                 adapter._delete_login_attempts_cached_email(
#                     self.request, email=email.email
#                 )

#         adapter.add_message(
#             self.request,
#             messages.SUCCESS,
#             "account/messages/password_changed.txt",
#         )
#         signals.password_reset.send(
#             sender=self.reset_user.__class__,
#             request=self.request,
#             user=self.reset_user,
#         )

#         if app_settings.LOGIN_ON_PASSWORD_RESET:
#             return perform_login(
#                 self.request,
#                 self.reset_user,
#                 email_verification=app_settings.EMAIL_VERIFICATION,
#             )

#         return super(PasswordResetFromKeyView, self).form_valid(form)


# password_reset_from_key = PasswordResetFromKeyView.as_view()
=======
from django.shortcuts import render
from rest_auth.models import TokenModel
from django.contrib.auth import  authenticate




>>>>>>> chat
