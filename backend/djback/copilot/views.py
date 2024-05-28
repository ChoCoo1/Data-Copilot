# app/views.py
from rest_framework import generics
from .models import CustomUser, DatabaseConnection
from .serializers import *
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
import pymysql


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def test_database_connection(request):
    sql_type = request.data.get('sqlType')
    sql_address = request.data.get('sqlAddress')
    sql_port = int(request.data.get('sqlPort'))
    sql_login_name = request.data.get('sqlLoginName')
    sql_pwd = request.data.get('sqlPwd')
    sql_name = request.data.get('sqlName')
    if sql_type == 'mysql':  # 修正了 if 条件判断的错误
        # 尝试连接数据库
        try:
            connection = pymysql.connect(
                host=sql_address,
                port=sql_port,
                user=sql_login_name,
                password=sql_pwd,
                database=sql_name
            )
            connection.close()
            return Response({'message': 'Connection successful'}, status=status.HTTP_200_OK)
        except Exception as e:  # 捕获 pymysql.Error 异常
            return Response({'message': 'Connection failed'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def save_database_connection(request):
    # 提取请求中的数据库连接信息
    sql_type = request.data.get('sqlType')
    sql_address = request.data.get('sqlAddress')
    sql_port = int(request.data.get('sqlPort'))
    sql_login_name = request.data.get('sqlLoginName')
    sql_pwd = request.data.get('sqlPwd')
    sql_name = request.data.get('sqlName')
    username = request.data.get('username')

    # 构建数据库连接实例并保存
    database_connection = DatabaseConnection(
        username=username,
        sql_type=sql_type,
        sql_address=sql_address,
        sql_port=sql_port,
        sql_login_name=sql_login_name,
        sql_pwd=sql_pwd,
        sql_name=sql_name
    )
    # 手动验证数据有效性
    is_valid, errors = database_connection.all_valid()
    if is_valid:
        database_connection.save()
        return Response({'message': 'Database connection saved successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': errors}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_database_connections(request):
    username = request.query_params.get('username')
    connections = DatabaseConnection.objects.filter(username=username)
    # 序列化数据
    serializer = PartialDatabaseConnectionSerializer(connections, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_database_connection(request):
    sql_id = request.data.get('sql_id');
    try:
        connection = DatabaseConnection.objects.filter(id=sql_id)
    except DatabaseConnection.DoesNotExist:
        return Response({'error': 'Database connection does not exist'}, status=status.HTTP_404_NOT_FOUND)

    connection.delete()
    return Response({'message': 'Database connection deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
