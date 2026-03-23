from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import PermissionDenied


class CorporateOnlyAdapter(DefaultSocialAccountAdapter):
    """
    Allows any Google account to log in.
    To restrict to a specific domain, uncomment and edit the block below.
    """

    def is_open_for_signup(self, request, sociallogin):
        return True

    # Uncomment below to restrict to a specific email domain:
    # def pre_social_login(self, request, sociallogin):
    #     email = sociallogin.account.extra_data.get('email', '')
    #     if not email.endswith('@yourdomain.com'):
    #         raise PermissionDenied("Only corporate accounts are allowed.")
