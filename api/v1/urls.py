from django.urls import path

from api.v1.auth.views import RegisView, LoginView, AuthOne, AuthTwo
from api.v1.sayt.ctg.views import CtgView


urlpatterns = [
    path('ctg/', CtgView.as_view()),
    path('ctg/<int:_id>/', CtgView.as_view()),

    path('auth/regis/', RegisView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/one/', AuthOne.as_view()),
    path('auth/two/', AuthTwo.as_view()),
]