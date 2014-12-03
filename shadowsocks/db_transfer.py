#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import time
import sys
from server_pool import ServerPool
import Config

import os 
sys.path.append(os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + '/../webfrontend/'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from shadowsocks.models import SSInstance

class DbTransfer(object):

    instance = None

    def __init__(self):
        self.last_get_transfer = {}

    @staticmethod
    def get_instance():
        if DbTransfer.instance is None:
            DbTransfer.instance = DbTransfer()
        return DbTransfer.instance

    def push_db_all_user(self):
        #更新用户流量到数据库
        last_transfer = self.last_get_transfer
        curr_transfer = ServerPool.get_instance().get_servers_transfer()
        #上次和本次的增量
        dt_transfer = {}
        for id in curr_transfer.keys():
            if id in last_transfer:
                if last_transfer[id][0] == curr_transfer[id][0] and last_transfer[id][1] == curr_transfer[id][1]:
                    continue
                elif curr_transfer[id][0] == 0 and curr_transfer[id][1] == 0:
                    continue
                elif last_transfer[id][0] <= curr_transfer[id][0] and \
                last_transfer[id][1] <= curr_transfer[id][1]:
                    dt_transfer[id] = [curr_transfer[id][0] - last_transfer[id][0],
                                       curr_transfer[id][1] - last_transfer[id][1]]
                else:
                    dt_transfer[id] = [curr_transfer[id][0], curr_transfer[id][1]]
            else:
                if curr_transfer[id][0] == 0 and curr_transfer[id][1] == 0:
                    continue
                dt_transfer[id] = [curr_transfer[id][0], curr_transfer[id][1]]

        self.last_get_transfer = curr_transfer

        for id in dt_transfer.keys():
            ins = SSInstance.objects.get(port=id)
            # print u
            ins.u += dt_transfer[id][0]
            ins.d += dt_transfer[id][1]
            # print u
            ins.save()

    @staticmethod
    def pull_db_all_user():
        #数据库所有用户信息
        return SSInstance.objects.values()

    @staticmethod
    def del_server_out_of_bound_safe(rows):
    #停止超流量的服务
    #启动没超流量的服务
        for row in rows:
            if ServerPool.get_instance().server_is_run(row['port']) > 0:
                if row['u'] + row['d'] >= row['transfer_enable'] or (not row['enable']):
                    logging.info('db stop server at port [%s]' % (row['port']))
                    ServerPool.get_instance().del_server(row['port'])
            elif ServerPool.get_instance().server_run_status(row['port']) is False:
                if row['switch'] and row['enable'] and  row['u'] + row['d'] < row['transfer_enable']:
                    logging.info('db start server at port [%s] pass [%s]' % (row['port'], row['passwd']))
                    ServerPool.get_instance().new_server(row['port'], row['passwd'])
    @staticmethod
    def thread_db():
        import socket
        import time
        timeout = 60
        socket.setdefaulttimeout(timeout)
        while True:
            #logging.warn('db loop')
            try:
                DbTransfer.get_instance().push_db_all_user()
                rows = DbTransfer.get_instance().pull_db_all_user()
                DbTransfer.del_server_out_of_bound_safe(rows)
            except Exception as e:
                logging.warn('db thread except:%s' % e)
            finally:
                time.sleep(15)


#SQLData.pull_db_all_user()
#print DbTransfer.get_instance().test()
