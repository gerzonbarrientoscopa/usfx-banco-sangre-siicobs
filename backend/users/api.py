import json
from datetime import date, timedelta
from django.contrib.auth import logout
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from users.models import Employee


class LoginTokenView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {'code': 200,
             'data': {
                 'roles': ['admin'],
                 'x_token': token.key,
                 'token': 'admin-token',
                 'user_id': user.pk,
                 'email': user.email,
                 'introduction': 'I am a super administrator',
                 'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                 'name': 'Super Admin'
             }})


class UserInfoView(ObtainAuthToken):
    # authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def get(self, request, *args, **kwargs):
        token = request.auth
        user = request.user

        if user.is_superuser:
            perm_tuple = Permission.objects.all()
            perm_tuple = [x.codename for x in perm_tuple]
            perm_tuple.insert(0, 'admin')
        else:
            perm_tuple = user.user_permissions.all() | Permission.objects.filter(group__user=user)
            perm_tuple = [x.codename for x in perm_tuple]

        employee = Employee.objects.filter(user_id=user.pk).first()
        employee_id = None
        name = 'Sin Nombre'
        min_date_edit = date.today()

        if employee:
            employee_id = employee.id
            name = str(employee)
            min_date_edit = date.today()

        employees = json.dumps([x.as_json() for x in Employee.objects.all()])
        employees = json.loads(employees)
        return Response(
            {'code': 200,
             'data': {
                 'roles': perm_tuple,
                 'x_token': token.key,
                 'token': 'admin-token',
                 'user_id': user.pk,
                 'employee_id': employee_id,
                 'employees': employees,
                 'email': user.email,
                 'introduction': '我是超级管理员',
                 'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                 'name': name,
                 'min_date_edit': min_date_edit
             }})


class LogoutUserView(ObtainAuthToken):
    queryset = User.objects.none()

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        logout(request)

        return Response({'code': 200, 'data': 'success'})

