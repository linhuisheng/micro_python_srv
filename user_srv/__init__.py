import os
import sys
from concurrent import futures
import logging
import grpc

# 解决 自动生成 proto 文件  模块导入问题
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
PROTO_DIR = ROOT_PATH + '/proto'
sys.path.append(PROTO_DIR)


# 日志拦截器
class LogInterceptors(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        print("请求start")
        # print(type(handler_call_details))
        resp = continuation(handler_call_details)
        print("请求end")
        return resp


class Applicaton():
    def __init__(self):
        logging.basicConfig()

    def serve(self):
        from user_srv.proto import user_pb2, user_pb2_grpc
        from user_srv.handler.user import UserServicer
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=(LogInterceptors(),))
        user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
        server.add_insecure_port('[::]:50052')
        print(f"启动服务:127.0.0.1:50052")
        server.start()
        server.wait_for_termination()


app = Applicaton()
