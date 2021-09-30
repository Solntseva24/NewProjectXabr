from datetime import timedelta
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.timezone import now
from xabr import settings


def get_activation_key_express():
    """функция для получения ключа активации пользователя"""

    return now() + timedelta(hours=48)


class XabrUser(AbstractUser):
    """модель пользователя"""

    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18, blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    email = models.EmailField(verbose_name='email', unique=True, blank=False)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))
    like_quantity = models.PositiveIntegerField('кол-во', default=0)
    is_active = models.BooleanField(verbose_name='активен/неактивен', default=True)
    is_staff = models.BooleanField(verbose_name='статус персонала', default=False)

    def is_activation_key_expired(self):
        """функция активации пользователя"""
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

    def send_verify_mail(self):
        """функция подтверждения учетной записи"""

        verify_link = reverse(
            'auth:verify',
            kwargs={
                'email': self.email,
                'activation_key': self.activation_key
            },
        )
        title = f'Подтверждение учетной записи {self.username}'
        message = f'Для подтверждения учетной записи {self.username} на портале ' \
                  f'{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

        return send_mail(title, message, settings.EMAIL_HOST_USER, [self.email], fail_silently=False)
