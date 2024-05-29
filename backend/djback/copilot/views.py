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
from openai import OpenAI

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="sk-4wJ2VKu3VL1fegJz5e3e930971B74e588343Cb774f9eB936",
    base_url="https://api.gpts.vin/v1",
)


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


# 大模型
# 获取一个数据库下的所有表的字段
def get_all_table_fields(username):
    connections = DatabaseConnection.objects.filter(username=username)
    serializer = DatabaseConnectionSerializer(connections, many=True)
    all_database_field = {}
    for connection_info in serializer.data:
        # 连接用户导入的数据库
        connection = pymysql.connect(
            host=connection_info['sql_address'],
            port=connection_info['sql_port'],
            user=connection_info['sql_login_name'],
            password=connection_info['sql_pwd'],
            database=connection_info['sql_name'],
            cursorclass=pymysql.cursors.DictCursor
        )

        all_table_fields = {}

        try:
            with connection.cursor() as cursor:
                # 查询所有表名
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                for table in tables:
                    table_name = table['Tables_in_' + connection_info['sql_name']]
                    # 查询表的字段信息
                    cursor.execute(f"DESCRIBE {table_name}")
                    fields = cursor.fetchall()
                    field_names = [field['Field'] for field in fields]
                    all_table_fields[table_name] = field_names
        finally:
            connection.close()
        all_database_field[connection_info['sql_name']] = all_table_fields
    return all_database_field


#  我想要查询datacopilot数据库中的copilot_customuser表中的所有信息
@api_view(['POST'])
def generate_sql_query(request):
    # 从前端获取搜索内容

    search_query = request.data.get('search_query', '')
    username = request.data.get('username', '')
    all_table_fields=get_all_table_fields(username)
    # 构建字段信息字符串
    fields_info = "\n".join(
        [f"Database: {db_name}, Table: {table_name}, Fields: {', '.join(fields)}"
         for db_name, tables in all_table_fields.items()
         for table_name, fields in tables.items()]
    )
    print(fields_info)
    # 使用搜索内容生成 SQL 查询语句的 Prompt
    prompt = (f"这里是数据库框架信息：\n{fields_info}\n\n"
              f"请你根据以下检索内容生成SQL查询语句：{search_query}")

    # 向 OpenAI 发送请求，生成 SQL 查询语句
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "你是一个数据库专家，熟悉所有sql语句，请你根据我的问题，认真输入sql语句，不要使用中文解释，请你对数据库中的字段进行充分分析，选择合适的字段进行数据库查询"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
        temperature=0.5
    )

    # 从 OpenAI 响应中获取生成的 SQL 查询语句
    # sql_query = completion.choices[0].message.content.strip()
    sql_query = completion
    print(sql_query)

    # 返回 SQL 查询语句给前端
    return Response({"sql_query": sql_query})
