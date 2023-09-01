# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 17:58:57 2023

@author: lijia
"""

from abc import abstractmethod

from pydantic import BaseModel, Field

# 成功
STATUS_SUCCEED = "succeed"
# 失败
STATUS_FAILED = "failed"
# 超时
STATUS_TIMEOUT = "timeout"
# 计算中
STATUS_PENDING = "penging"
# 队列中
STATUS_INQUEUE = "in_queue"
# 新建
STATUS_NEW = "new"

class Req:
    def __init__(self, url, param):
        self.url = url;
        self.param = param;

class AbstractModel(BaseModel):
    async_mode: bool = Field(False)

class IDbOperator:

    @abstractmethod
    def getEngine(self):
        pass

    @abstractmethod
    def createTable(self):
        pass

    @abstractmethod
    def dropTable(self, table_name):
        pass

    @abstractmethod
    def insertOne(self, data):
        pass

    @abstractmethod
    def beginTx(self):
        pass

    @abstractmethod
    def rollbackTx(self, session):
        pass

    @abstractmethod
    def commitTx(self, session):
        pass

    @abstractmethod
    def getSession(self):
        pass

    @abstractmethod
    def closeSession(self, session):
        pass

    @abstractmethod
    def doInTransaction(self, func):
        pass

    @abstractmethod
    def executeRawSql(self, rawSql: str):
        pass

class IPlatformConfig:

    def get_model_name(self):
        pass

    def get_root_path(self):
        pass

    def get_logfile_path(self):
        pass

    def get_uploadfile_path(self):
        pass

    def get_requests_path(self):
        pass

    def db_password(self) -> str:
        pass

    def db_user(self):
        pass

    def db_host(self):
        pass

    def db_port(self):
        pass

    def db_name(self):
        pass

    def db_type(self):
        pass

    def get_config(self, config_name):
        pass

class IContext:

    '''
    每个请求对应一个context对象，提供数据库操作，文件操作等基本功能，日志操作等
    '''
    @abstractmethod
    def new_dboperator(self, db_config) -> IDbOperator:
        '''
        创建一个新的数据库操作器
        '''
        pass

    @abstractmethod
    def get_attachment_path(self, attachment_id):
        '''
        根据附件ID获取附件绝对路径
        :param attachment_id:
        :return:
        '''
        pass

    @abstractmethod
    def save_attachment(self, filepath:str)->str:
        """
        保存附件返回附件ID
        :param filepath:
        :return: None or attach_id
        """
        pass

    @abstractmethod
    def get_root_path(self):
        '''
        返回请求对应的根目录
        '''
        pass
    
    @abstractmethod
    def get_logger(self, logger_name: str = None):
        '''
        获取日志记录器
        '''
        pass

    @abstractmethod
    def save_result(self, result: dict, succeed: bool)->bool:
        pass

    @abstractmethod
    def update_request_status(self, status: int)->bool:
        pass

    @abstractmethod
    def in_queue(self):
        pass

    @abstractmethod
    def app_config(self) -> IPlatformConfig:
        '''
        获取应用配置, 最从协议：IPlatformConfig
        '''
        pass

    def raw_config(self):
        pass


