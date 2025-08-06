import requests
from urllib.parse import urlencode, parse_qs
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core import signing
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic.base import RedirectView

User = get_user_model()

NAVER_CALLBACK_URL = '/oauth/naver/callback'
NAVER_STATE = 'naver_login'
NAVER_LOGIN_URL = 'https://nid.naver.com/oauth2.0/authorize'    # API 요청 URL
NAVER_TOKEN_URL = 'https://nid.naver.com/oauth2.0/token'
NAVER_PROFILE_URL = 'https://openapi.naver.com/v1/nid/me'


class NaverLoginRedirectView(RedirectView) :
    def get_redirect_url(self, *args, **kwargs):
        domain = self.request.scheme + '://' + self.request.META.get('HTTP_HOST','')
        # scheme : 요청의 프로토콜 반환 (http, https)
        # self.request.META.get('HTTP_HOST', '') : 요청 헤더 중 Host 값을 가져옴 ('127.0.0.1:8000' 같은 값)

        callback_url = domain + NAVER_CALLBACK_URL
        state = signing.dumps(NAVER_STATE)  # state 값 암호화

        # API 필수 요청 변수
        params = {
            'response_type': 'code',
            'client_id' : settings.NAVER_CLIENT_ID,
            'redirect_uri' : callback_url,
            'state' : state
        }

        # print(f'{NAVER_LOGIN_URL}?{urlencode(params)}')
        return f'{NAVER_LOGIN_URL}?{urlencode(params)}'
        # urlencode : 딕셔너리 형태의 데이터를 URL 쿼리 문자열로 인코딩


def naver_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    if NAVER_STATE != signing.loads(state):
        raise Http404

    access_token = get_naver_access_token(code, state)

    print('token request', result)
    profile_response = get_naver_profile(access_token)

    print('profile request', profile_response)
    email = profile_response.get('email')

    user = User.objects.filter(email=email).first()

    if user :
        if not user.is_active :
            user.is_active = True
            user.save()
        login(request, user)
        return redirect('main')

    # 사용자 정보가 없으면 생성해주면서 닉네임 입력하는 창으로 보내줘야 함 (현재 요청에서는 Nickname값을 가져올 수 없음)
    return redirect(
        reverse('oauth:nickname') + f'?access_token={access_token}'
    )

def get_naver_access_token(code, state):
    params = {
        'grant_type': 'authorization_code',
        'client_id': settings.NAVER_CLIENT_ID,
        'client_secret': settings.NAVER_SECRET,
        'code': code,
        'state': state
    }

    response = requests.get(NAVER_TOKEN_URL, params=params)
    result = response.json()    # return값으로 토큰들이 들어옴
    access_token = result.get('access_token')


# 닉네임을 입력받아 사용자를 생성해주는 function view
def oauth_nickname(request):
    access_token = request.GET.get('access_token')
    if not access_token :
        return redirect('login')

    from member.forms import NicknameForm
    form = NicknameForm(request.POST or None)

    if form.is_valid() :
        user = form.save(commit=False)  # form에서 Nickname만 받았으므로 nickname만 있는 상태

        profile = get_naver_profile(access_token)
        email = profile.get('email')

        if User.objects.filter(email=email).exists() :
            raise Http404

        user.email = email

        user.is_active = True
        user.set_password(User.objects.make_random_password())  # 비워놔도 되는데 보안을 위해 랜덤 패스워드 넣어줌
        user.save()

        login(request, user)
        return redirect('main')

    return render(request, 'auth/nickname.html', {'form': form})


# 토큰으로 유저 프로필 정보 요청
def get_naver_profile(access_token):
    # Authorization 헤더에 토큰을 실어 사용자 정보 요청
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(NAVER_PROFILE_URL, headers=headers)

    if response.status_code != 200 :
        raise Http404

    result = response.json()
    return result.get('response')



NAVER_CALLBACK_URL = '/oauth/naver/callback'
NAVER_STATE = 'naver_login'
NAVER_LOGIN_URL = 'https://nid.naver.com/oauth2.0/authorize'    # API 요청 URL
NAVER_TOKEN_URL = 'https://nid.naver.com/oauth2.0/token'
NAVER_PROFILE_URL = 'https://openapi.naver.com/v1/nid/me'

GITHUB_CALLBACK_URL = '/oauth/github/callback'
GITHUB_STATE = 'github_login'
GITHUB_LOGIN_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_PROFILE_URL = "https://api.github.com/user"


class NaverLoginRedirectView(RedirectView) :
    def get_redirect_url(self, *args, **kwargs):
        domain = self.request.scheme + '://' + self.request.META.get('HTTP_HOST','')
        # scheme : 요청의 프로토콜 반환 (http, https)
        # self.request.META.get('HTTP_HOST', '') : 요청 헤더 중 Host 값을 가져옴 ('127.0.0.1:8000' 같은 값)

        callback_url = domain + NAVER_CALLBACK_URL
        state = signing.dumps(NAVER_STATE)  # state 값 암호화

        # API 필수 요청 변수
        params = {
            'response_type': 'code',
            'client_id' : settings.NAVER_CLIENT_ID,
            'redirect_uri' : callback_url,
            'state' : state
        }

        # print(f'{NAVER_LOGIN_URL}?{urlencode(params)}')
        return f'{NAVER_LOGIN_URL}?{urlencode(params)}'
        # urlencode : 딕셔너리 형태의 데이터를 URL 쿼리 문자열로 인코딩


def naver_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    if NAVER_STATE != signing.loads(state):
        raise Http404

    access_token = get_naver_access_token(code, state)
    profile_response = get_naver_profile(access_token)

    print('profile request', profile_response)
    email = profile_response.get('email')

    user = User.objects.filter(email=email).first()

    if user :
        if not user.is_active :
            user.is_active = True
            user.save()
        login(request, user)
        return redirect('main')

    # 사용자 정보가 없으면 생성해주면서 닉네임 입력하는 창으로 보내줘야 함 (현재 요청에서는 Nickname값을 가져올 수 없음)
    return redirect(
        reverse('oauth:nickname') + f'?access_token={access_token}&oauth=naver'
    )

def get_naver_access_token(code, state):
    params = {
        'grant_type': 'authorization_code',
        'client_id': settings.NAVER_CLIENT_ID,
        'client_secret': settings.NAVER_SECRET,
        'code': code,
        'state': state
    }

    response = requests.get(NAVER_TOKEN_URL, params=params)
    result = response.json()    # return값으로 토큰들이 들어옴
    access_token = result.get('access_token')

# 토큰으로 유저 프로필 정보 요청
def get_naver_profile(access_token):
    # Authorization 헤더에 토큰을 실어 사용자 정보 요청
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(NAVER_PROFILE_URL, headers=headers)

    if response.status_code != 200 :
        raise Http404

    result = response.json()
    return result.get('response')



class GithubLoginRedirectView(RedirectView) :
    def get_redirect_url(self, *args, **kwargs):
        domain = self.request.scheme + '://' + self.request.META.get('HTTP_HOST','')
        # scheme : 요청의 프로토콜 반환 (http, https)
        # self.request.META.get('HTTP_HOST', '') : 요청 헤더 중 Host 값을 가져옴 ('127.0.0.1:8000' 같은 값)

        callback_url = domain + GITHUB_CALLBACK_URL
        state = signing.dumps(GITHUB_STATE)  # state 값 암호화

        # API 필수 요청 변수
        params = {
            'response_type': 'code',
            'client_id' : settings.GITHUB_CLIENT_ID,
            'redirect_uri' : callback_url,
            'state' : state
        }

        return f'{GITHUB_LOGIN_URL}?{urlencode(params)}&oauth=github'
        # urlencode : 딕셔너리 형태의 데이터를 URL 쿼리 문자열로 인코딩


def github_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    if GITHUB_STATE != signing.loads(state):
        raise Http404

    access_token = get_github_access_token(code, state)
    if not access_token :
        raise Http404

    profile_response = get_github_profile(access_token)

    print('profile request', profile_response)
    email = profile_response.get('email')

    user = User.objects.filter(email=email).first()

    if user :
        if not user.is_active :
            user.is_active = True
            user.save()
        login(request, user)
        return redirect('main')

    # 사용자 정보가 없으면 생성해주면서 닉네임 입력하는 창으로 보내줘야 함 (현재 요청에서는 Nickname값을 가져올 수 없음)
    return redirect(
        reverse('oauth:nickname') + f'?access_token={access_token}&oauth=github'
    )


def get_github_access_token(code, state):
    params = {
        'grant_type': 'authorization_code',
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_SECRET,
        'code': code,
        'state': state
    }

    response = requests.get(GITHUB_TOKEN_URL, params=params)

    response_str = response.content.decode()    # 바이너리 형태의 response를 문자열 형태로 변환
    response_dict = parse_qs(response_str)      # parsing해서 딕셔너리 형태로 변환
    access_token = response_dict.get('access_token', [])[0]

    return access_token

# 토큰으로 유저 프로필 정보 요청
def get_github_profile(access_token):
    # Authorization 헤더에 토큰을 실어 사용자 정보 요청
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(GITHUB_PROFILE_URL, headers=headers)

    if response.status_code != 200 :
        raise Http404

    result = response.json()

    # github에서 이메일을 private으로 설정하면 이메일 값을 안 줌
    # 이메일이 None일 때 임의의 이메일 넣어주기
    if not result.get('email'):
        result['email'] = f'{result["login"]}@id.github.com'

    return result   # github는 바로 데이터가 들어오기 때문에 .get('response') 해줄 필요 없음


# 닉네임을 입력받아 사용자를 생성해주는 function view
def oauth_nickname(request):
    access_token = request.GET.get('access_token')
    oauth = request.GET.get('oauth')

    if not access_token or oauth not in ['github', 'naver']:
        return redirect('login')

    from member.forms import NicknameForm
    form = NicknameForm(request.POST or None)

    if form.is_valid() :
        user = form.save(commit=False)  # form에서 Nickname만 받았으므로 nickname만 있는 상태

        if oauth == 'naver' :
            profile = get_naver_profile(access_token)
        else :
            profile = get_github_profile(access_token)
        email = profile.get('email')

        if User.objects.filter(email=email).exists() :
            raise Http404

        user.email = email

        user.is_active = True
        user.set_password(User.objects.make_random_password())  # 비워놔도 되는데 보안을 위해 랜덤 패스워드 넣어줌
        user.save()

        login(request, user)
        return redirect('main')

    return render(request, 'auth/nickname.html', {'form': form})

