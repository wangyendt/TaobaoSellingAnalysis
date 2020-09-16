#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:  wangye
@file: main.py 
@time: 2020/09/16
@contact: wangye.hope@gmail.com
@site:  
@software: PyCharm 
"""

from tools import *
import pandas as pd
import re


def extract_taste(info: str):
    res = re.findall(r'口味：([\u4e00-\u9fa5]+)', info)
    if not res: return ''
    return res[0]


def extract_sending_num(info: str):
    res = re.findall(r'【加送\d+袋发(\d+)袋】', info)
    if res:
        return int(res[0])
    else:
        res = re.findall(r'\*(\d+)【', info)
        if not res:
            return 0
        else:
            return int(res[0])


def main():
    remained_column = ['订单编号', '买家会员名', '买家支付宝账号', '支付单号',
                       '买家实际支付金额', '订单状态', '收货人姓名', '收货地址 ',
                       '联系手机', '订单付款时间 ', '物流单号 ']
    order_list_file = list_all_files(root, [date, '.xlsx'])
    if not order_list_file:
        print('未找到订单报表')
        return
    order_list_file = order_list_file[0]
    item_list_file = list_all_files(root, [date, '.csv'])
    if not item_list_file:
        print('未找到宝贝报表')
        return
    item_list_file = item_list_file[0]

    with open(order_list_file, 'rb') as olf:
        order_data = pd.read_excel(olf, dtype=str)
        order_data = order_data[remained_column]
    with open(item_list_file, 'rb') as ilf:
        item_data = pd.read_csv(ilf, dtype=str, encoding="gbk")
        item_data['订单编号'] = item_data['订单编号'].map(lambda x: re.findall(r'"(\d+)"', x)[0])
        item_data['口味'] = item_data['商品属性'].map(extract_taste)
        item_data['发货数量'] = item_data['商品属性'].map(extract_sending_num)
        item_data = item_data[['订单编号', '口味', '发货数量']]
    result = pd.merge(order_data, item_data, 'outer', ['订单编号'])
    result = result.loc[result['订单状态'] == '卖家已发货，等待买家确认', :]
    result['发货日期'] = delivering_date

    save_dir = 'result'
    save_file_name = order_list_file[order_list_file.rindex('\\') + 1:order_list_file.rindex('.')]
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    result.to_excel(f'{save_dir}/{save_file_name}.xlsx')
    print(f'结果已经保存到{save_dir}/{save_file_name}.xlsx')


if __name__ == '__main__':
    root = 'rawdata'
    date = '20200916'
    delivering_date = '20200914->20200915'
    main()
