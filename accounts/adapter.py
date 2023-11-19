from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        # 추가 정보 설정
        extra_data = sociallogin.account.extra_data['kakao_account']['profile']
        user.nickname = extra_data.get('nickname')
        user.profile_image = extra_data.get('profile_image_url')

        return user

    # def save_user(self, request, sociallogin, form=None):
    #     user = super(CustomSocialAccountAdapter, self).save_user(request, sociallogin, form=None)
    #     user_data = sociallogin.account.extra_data
    #     user.oid = user_data.get('id')
    #     user.username = user_data.get('properties', {}).get('thumbnail_image_url', '')
    #     print(user.oid)
    #     user.save()
    #     return user
