from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from utils.models import TimeStampModel


class UserManager(BaseUserManager) :
    def create_user(self, email, password) :
        if not email :
            raise ValueError('올바른 이메일을 입력하세요.')

        # self.model = User
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password) # password 해시화
        user.is_active = False
        user.save(using=self._db)
        return user

    # python manage.py createsuperuser 할 때 호출되는 함수
    def create_superuser(self, email, password) :
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser) :
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
    )
    is_active = models.BooleanField(default=False)  # 이메일 인증을 받으면 True가 되고 로그인 가능하도록 default False
    is_admin = models.BooleanField(default=False)
    nickname = models.CharField('nickname', max_length=20, unique=True)
    following = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers',
        through='UserFollowing', through_fields=('from_user', 'to_user')
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'    # username 대신 email 사용
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = f'{verbose_name} 목록'

    # get_full_name & get_short_name => 영어 이름에서 성하고 이름 합쳐주는 역할
    # 이름이 없으니 nickname으로 퉁친다...
    def get_full_name(self) :
        return self.nickname
    def get_short_name(self) :
        return self.nickname

    def __str__(self) :
        return self.nickname

    # 아래로 기본 모듈들 오버라이드 해줌

    def has_perm(self, perm, obj=None) :
        return True

    def has_module_perms(self, app_label) :
        return True

    # @property => 메서드를 변수처럼 사용할 수 있게 해줌
    # user.is_staff() 가 아니라 user.is_staff 로 사용
    @property
    def is_staff(self) :
        return self.is_admin

    @property
    def is_superuser(self) :
        return self.is_admin

class UserFollowing(TimeStampModel) :
    # 같은 테이블을 참조하는 외래키가 둘이기 때문에 반드시 related_name 설정해줘야 함!
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_followers')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_following')    # 팔로우 하는 사람

    class Meta:
        unique_together = ('to_user', 'from_user')  # 두개를 합친 쌍이 Unique => 중복 방지
        # to_user: 1, from_user: 2
        # to_user: 1, from_user: 3
        # to_user: 2, from_user: 1 => ok
        # to_user: 1, from_user: 2 => 오류
