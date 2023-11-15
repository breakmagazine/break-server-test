import requests
from django.shortcuts import redirect
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from json.decoder import JSONDecodeError
from rest_framework import status
from rest_framework.response import Response
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount

from breakserver.settings import secrets
from .models import CustomUser


BASE_URL = 'http://127.0.0.1:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'accounts/kakao/callback/'

state = getattr(settings, 'STATE')

def kakao_login(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )


def kakao_callback(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    code = request.GET.get("code")
    redirect_uri = KAKAO_CALLBACK_URI
    client_secret = secrets['SECRET_KEY']

    """
    Access Token Request
    """

    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")

    """
    Profile Request
    """

    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    profile_json = profile_request.json()
    error = profile_json.get("error")
    if error is not None:
        print(error)
        raise JSONDecodeError(error)
    user_oid = profile_json.get('id')
    kakao_account = profile_json.get('kakao_account')
    # print(user_oid) #user_id는 유저의 카카오 아이디
    # print(kakao_account) #nickname, thumbnail_image_url 제공

    """
    Signup or Signin Request
    """
    try:
        user = CustomUser.objects.get(oid=user_oid)
        #user가 존재할 때 Logic 팔요


        # # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        # # 다른 SNS로 가입된 유저
        # social_user = SocialAccount.objects.get(user=user)
        # if social_user is None:
        #     return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        # if social_user.provider != 'kakao':
        #     return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # # 기존에 Google로 가입된 유저
        # data = {'access_token': access_token, 'code': code}
        # accept = requests.post(
        #     f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        # accept_status = accept.status_code
        # if accept_status != 200:
        #     return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        # accept_json = accept.json()
        # accept_json.pop('user', None)
        # return JsonResponse(accept_json)
    except CustomUser.DoesNotExist:
        print("CustomUser.DoesNotExist")
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        print(data)
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/",
            data=data
        )


        accept_status = accept.status_code
        print(accept_status)
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)

        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI
