# app/views.py
from rest_framework import generics
from .serializers import *
from .models import *
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from translate import Translator

from rest_framework.decorators import api_view
import pymysql
import os

# 初始化 OpenAI 客户端

API_SECRET_KEY = "sk-4wJ2VKu3VL1fegJz5e3e930971B74e588343Cb774f9eB936"
BASE_URL = "https://api.gpts.vin/v1"

os.environ["OPENAI_API_KEY"] = API_SECRET_KEY
os.environ["OPENAI_API_BASE"] = BASE_URL


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


@api_view(['GET'])
def get_database_name(request):
    username = request.query_params.get('username')
    connections = DatabaseConnection.objects.filter(username=username)
    # 序列化数据
    serializer = DatabaseNameSerializer(connections, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 删除数据库连接
@api_view(['DELETE'])
def delete_database_connection(request):
    sql_id = request.data.get('sql_id');
    try:
        connection = DatabaseConnection.objects.filter(id=sql_id)
    except DatabaseConnection.DoesNotExist:
        return Response({'error': 'Database connection does not exist'}, status=status.HTTP_404_NOT_FOUND)

    connection.delete()
    return Response({'message': 'Database connection deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# 搜索历史
@api_view(['POST'])
def add_search_history(request):
    username = request.data.get('username', '')
    search_query = request.data.get('search_query', '')
    search_sql_name = request.data.get('search_sql_name', '')
    SearchHistory.objects.create(username=username, search_query=search_query, search_sql_name=search_sql_name)
    return Response({'message': 'Search history saved successfully'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_search_history(request):
    username = request.query_params.get('username')
    history = SearchHistory.objects.filter(username=username)
    serializer = SearchHistorySerializer(history, many=True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_password(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        user = CustomUser.objects.get(username=username)
        user.set_password(password)
        user.save()
        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def update_phone(request):
    username = request.data.get('username')
    phone = request.data.get('phone')
    try:
        user = CustomUser.objects.get(username=username)
        user.phone = phone
        user.save()
        return Response({'message': 'Phone number updated successfully'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 大模型
@api_view(['POST'])
def generate_sql_query(request):
    # 从前端获取搜索内容
    search_query = request.data.get('search_query', '')
    username = request.data.get('username', '')
    sql_name = request.data.get('sql_name', '')
    search_query = search_query + '不要使用LIMIT命令，并且如果要使用聚合函数，请把使用聚合函数的变量放在select作为最后一个变量，把可以识别每个列的变量作为select的第一个变量。'
    search_query = Translator(from_lang="ZH", to_lang="EN-US").translate(search_query)

    # 初始化LangChain模型并指定API URL
    llm = ChatOpenAI(model="gpt-3.5-turbo")

    # 根据sql_name获取数据库连接信息
    connections = DatabaseConnection.objects.filter(username=username, sql_name=sql_name)
    if not connections.exists():
        return Response({"error": "Database connection not found."}, status=404)
    serializer = DatabaseConnectionSerializer(connections, many=True)
    connection_info = serializer.data[0]  # 假设只有一个数据库连接

    # 创建SQLDatabase对象
    db_uri = f"mysql+pymysql://{connection_info['sql_login_name']}:{connection_info['sql_pwd']}@" \
             f"{connection_info['sql_address']}:{connection_info['sql_port']}/{connection_info['sql_name']}"
    db = SQLDatabase.from_uri(db_uri)

    # 创建SQL查询链
    sql_query_chain = create_sql_query_chain(llm, db)

    # 生成SQL查询
    sql_query = sql_query_chain.invoke({"question": search_query})

    if not sql_query.lower().startswith('select'):
        return Response({"error": "Invalid SQL query generated."}, status=400)
        # 将查询语句中的换行符替换为空格

    sql_query = sql_query.replace('\n', ' ')
    # 截断在第一个分号处
    sql_query = sql_query.split(';')[0] + ';'

    can_chart = False
    aggregate_functions = ['COUNT', 'SUM', 'AVG']  # 可能的聚合函数列表

    for func in aggregate_functions:
        if func in sql_query.upper():  # 不区分大小写地检查是否包含聚合函数
            can_chart = True
    # 使用pymysql执行查询并获取结果
    try:
        connection = pymysql.connect(
            host=connection_info['sql_address'],
            port=int(connection_info['sql_port']),
            user=connection_info['sql_login_name'],
            password=connection_info['sql_pwd'],
            database=connection_info['sql_name'],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            results = cursor.fetchall()
            column_names = cursor.description
        connection.close()

        # 获取列名
        column_names = [col[0] for col in column_names]
    except pymysql.MySQLError as e:
        return Response({"error": str(e)}, status=500)
    return Response({"sql_query": sql_query, "columns": column_names, "results": results, "shouldChart": can_chart})
