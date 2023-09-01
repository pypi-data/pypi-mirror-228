import os
from abc import ABC, abstractmethod
from functools import wraps

from fastapi import HTTPException
from starlette.requests import Request

from plugins_support import IModuleCaller, IRouterRegister


class PluginContext:
    pass

def get_request(request: Request):
    return request

class PluginInterface(ABC):
    def __init__(self,  module_caller: IModuleCaller, route_register: IRouterRegister):
        self.module_caller = module_caller
        self.route_register = route_register
        self.initialize()

    def register_api(self, *args, **kwargs):
        s_router, func_name = args
        plugin_name = self.get_namespace()
        if not plugin_name:
            plugin_name = self.__class__.__name__.lower()
        router = f"/{plugin_name}{s_router}"
        if self.get_tags():
            # 所有router配置同样的tags
            if isinstance(self.get_tags(), list):
                kwargs.update({"tags": self.get_tags()})
            # 配置每个router一个tags
            elif isinstance(self.get_tags(), dict):
                tags = self.get_tags().get(s_router)
                if tags and isinstance(tags, list):
                    kwargs.update({"tags": tags})

        self.route_register.register_api(router, func_name, **kwargs)

    @abstractmethod
    def initialize(self):
        pass

    def after_plugin_loaded(self, config):
        """
            插件初始化加载配置完成以后框架进行回调
        """
        pass

    def get_datasource_configs(self, config) -> list:
        """
            获取所有数据源配置
        """
        pass

    def config_files(self):
        pass

    def router(self):
        return self.route_register.router()

    # def my_decorator(arg1, arg2):
    #     def decorator(func):
    #         def wrapper(*args, **kwargs):
    #             print(f"Before call with arguments {arg1} and {arg2}")
    #             result = func(*args, **kwargs)
    #             print(f"After call with arguments {arg1} and {arg2}")
    #             return result
    #
    #         return wrapper
    #
    #     return decorator


    # 标注为service方法
    @staticmethod
    def service(caculator_clazz):
        def servicemethod(func: callable):
            # 使用functools.wraps标注，使得方法签名不被修改
            @wraps(func)
            def wrapfunc(self, *args, **kwargs):
                args = []
                request = None
                for arg in list(kwargs.values()):
                    if not isinstance(arg, Request):
                        args.append(arg)
                    else:
                        request = arg
                if request is None:
                    raise HTTPException(4004, "接口声明有问题，缺少request参数")
                async_mode = "false" != request.query_params.get("async_mode")
                args.append(async_mode)
                args.append(caculator_clazz)
                args.append(request)
                # args = tuple(args)
                # 从request中获取async_mode参数, async_mode通过depends添加到所有接口的参数表中
                # 传参使用 *args, **kwargs 进行解包处理
                return self.module_caller.call_module(*args, **kwargs)
            return wrapfunc
        return servicemethod


    @abstractmethod
    def get_namespace(self):
        """
        :return: 命名空间作为router前缀暴露
        """
        pass

    def get_tags(self):
        """
        接口的标签，可用于接口文档页面上的接口分类显示
        :return: 返回: list 或 dict
        """
        pass

    # @abstractmethod
    # def initialize(self, module_caller: IModuleCaller):
    #     pass
    #
    # @abstractmethod
    # def process(self, data):
    #     pass
