from django.urls import path, include
from users.api import LoginTokenView, UserInfoView, LogoutUserView

urlpatterns = [
    path('api/v1/user/', include([
        path('login', LoginTokenView.as_view()),
        path('info', UserInfoView.as_view()),
        path('logout', LogoutUserView.as_view()),
    ]))
]
