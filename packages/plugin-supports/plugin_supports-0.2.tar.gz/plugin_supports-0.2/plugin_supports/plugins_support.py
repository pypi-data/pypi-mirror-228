from fastapi import APIRouter

from context import *

# 提供路由注册服务
class IRouterRegister:

    @abstractmethod
    def register_api(self, router, func_name, **kwargs):
        pass

    @abstractmethod
    def router(self) -> APIRouter:
        pass


class AbstCalculator:
    '''
    抽象算子，封装了一次计算所需的上下文数据，所有模型方法需要继承该类，进行封装处理
    '''
    def __init__(self,
                 context: IContext,
                 async_process:bool=True,

                 ):
        self.async_process = async_process
        self.context = context

    # 提交给线程池方法必须携带args, kwargs两个参数
    def do_task(self, *args, **kwargs):
        '''
            params: 是一个tuple, 类型为：((),{}),
            params[0]是一个元组，按次序存放非命名参数；
            params[1]是一个字典，存放命名参数；
            '''
        # 1. 解析参数
        # args_tuple = params_tuple[0]
        # kargs_dict = params_tuple[1]
        # context = kargs_dict['context']
        # setContext(context)
        # ############################
        # print("-> 1. 在这里添加获取参数的逻辑 ############")
        log = self.context.get_logger()
        log.info(f"开始计算：{self.context.req_id}, 状态设置为：pending")
        try:
            self.context.updateRequestStatus(STATUS_PENDING)
            # 2、处理业务逻辑算法
            result = self.call_model_method()
            if not isinstance(result, dict):
                print("-> ERROR: result 模块计算的返回值, 应当是一个 dict");
                raise TypeError("result is not a dict")
            self.context.saveResult(result, True)
            log.info(f"计算成功：{self.context.req_id}, 状态设置为：succeed")
            return result
        except BaseException as err:
            traceback.print_exc()
            result = {"error": str(err)}
            self.context.saveResult({"error": str(err)}, False)
            log.error(f"计算失败：{self.context.req_id}, 状态设置为：failed", err)
            return result
        # finally:
            # 3、保存结果, 结果为dict类型
            # setContext(None)

    @abstractmethod
    def call_model_method(self):
        '''
        子类继承，实现该方法，一个子类对应一个模型方法，如果有多个模型方法，请定义多个子类
        '''
        pass

class AbstModule(AbstCalculator):

    def __init__(self,
                 context: IContext,
                 async_process: bool = True,
                 ):
        super().__init__(context, async_process)

    def call_model_method(self, id):
        '''
        子类继承，实现该方法，一个子类对应一个模型方法，如果有多个模型方法，请定义多个子类
        '''
        raise Exception("method not implemented exception")


class IModuleCaller:
    # @abstractmethod
    # def call_module(self, params, module: AbstModule):
    #     pass

    @abstractmethod
    def call_module(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    obj = AbstModule(None, False)
    print(obj is None)
    obj.call_model_method("1234")
