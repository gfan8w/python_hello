from wsgiref.simple_server import make_server

from wsgi.WSGI_sample import application

# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('', 8000, application)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()

# # 访问 http://localhost:8000/ddl 进行测试

