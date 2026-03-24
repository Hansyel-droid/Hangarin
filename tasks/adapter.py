from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CorporateOnlyAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        return True

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # Ensure Google login users are NEVER staff or superusers
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user