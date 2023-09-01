# -*- coding: utf-8 -*- 
# @Time : 2023/8/16 上午9:36
# @Author : zhaomeng
# @File : kjutils.py.py
# @desc:  处理规格格式
import re
from pprint import pprint


class Kjutils(object):
    def __init__(self, string: dict, exclude: list = None, lower_fields: list = None, comma_fields: list = None,
                 process_fields: list = None, units: list = None):
        """
        字符串处理中间件
        @param string: 处理的json数据
        @param exclude: 不需要处理空格的字段
        @param lower_fields: 需要小写的字段
        """

        if exclude is None:
            # 默认需要过滤字符串空格的字段列表
            exclude = ['price', "purity", "specs"]
        if lower_fields is None:
            # 需要转成小写的字段默认为specs规格
            lower_fields = ["specs"]
        if comma_fields is None:
            # 需要去除逗号的字段默认为price规格
            comma_fields = ["price"]
        if process_fields is None:
            # 排除特殊字符处理
            process_fields = ["DMSO"]
        if units is None:
            # 单位
            units = ["mg", "g"]
        self.result = string
        self.exclude = exclude
        self.comma_fields = comma_fields
        self.lower_fields = lower_fields
        self.process_fields = process_fields
        self.units = units

    @property
    def filter_str(self):
        """
        specs过滤特殊字符串,返回False不做处理,True做处理
        @return:
        """
        fields_list = []

        for d in self.process_fields:
            if d in self.result.get("specs", ""):
                fields_list.append(False)
            else:
                fields_list.append(True)
        return any(fields_list)

    def filter_l_r(self):
        """
        字典的值去除左右空格
        @param value:
        @return:
        """
        self.result = {_: val.strip() for _, val in self.result.items() if val}

        # print(self.result)

    @property
    def filter_vals_g_mg(self):
        # 以g/mg结尾的规格数据，去除空格
        field = self.result.get("specs").lower()
        return any([field.endswith(unit.lower()) for unit in self.units])

    def filter_vals(self):
        """
        过滤字段，去除空格
        @param exclude:
        @return:
        """
        patter = re.compile(r"\s")
        info = {_: re.sub(patter, '', val) for _, val in self.result.items() if
                _ in self.lower_fields and val != None and self.filter_vals_g_mg}
        self.result.update(info)

        # pprint(self.result)

    def filter_comma(self):
        """
        去除字段中存在的逗号
        @return:
        """
        patter = re.compile(r",")
        info = {_: re.sub(patter, '', val) for _, val in self.result.items() if _ in self.comma_fields}
        self.result.update(info)

        # pprint(self.result)

    def filter_int(self):
        """
        规格及货号数据取整
        去除小数点后面的只有一位的0
        @return:
        """
        try:
            if self.filter_str:
                patter = re.compile(r'\d+')
                # patter1 = re.compile(r"[a-zA-Z]") # 不能匹配 μ
                val = patter.findall(self.result.get('specs'))
                val = [s for s in val if int(s) >= 0]
                val = '.'.join(val)
                # print(val)
                unit = self.result.get('specs').split(val.strip())[-1]
                if "." in val:
                    first_val = val.strip().split('.')[0]
                    val = val.strip().split('.')[-1] if "." in val else val.strip()
                    # val = first_val + "." + val if val != str(0) else first_val
                    val = first_val + "." + val if int(val) else first_val

                specs = str(val) + ''.join(unit)
                goods_id = '-'.join(self.result.get("goods_id").split('-')[0:-1])
                info = {"specs": specs, 'goods_id': goods_id + "-" + specs.lower()}
                # info = {"specs": specs}
                self.result.update(info)
            else:
                pass
        except ValueError:
            pass

    def filter_lower(self):
        """
        字段小写,去除/
        @param string_list: []
        @return:
        """

        self.result.update(
            {_: val.lower() for _, val in self.result.items() if _ in self.lower_fields and self.filter_str})
        self.result.update({_: val.replace('/', '') for _, val in self.result.items() if _ in self.lower_fields})

        # pprint(self.result)

    def int_to_str(self):
        self.result = {_: str(val).strip() for _, val in self.result.items() if val}

    def process_item(self):
        self.int_to_str()  # 数字转字符串
        self.filter_l_r()  # 去除左右空格
        self.filter_vals()  # 去除所有的空格
        self.filter_comma()  # 去除逗号
        self.filter_int()  # specs去除小数点后的0
        self.filter_lower()  # 转成小写

        return self.result


if __name__ == '__main__':
    # value = {'goods_id': '0109160017-10 mM * 1 mL in DMSO ', 'productname': "3-bromo-[1,1'-biphenyl]-4-ol", 'cas': '92-03-5',
    #          'purity': ' 95% ', 'specs': '  50MG(COLL)   ', 'price': '$58.00', 'stock': '8700mg',
    #          'source': 'otavachemicals',
    #          'mdl': 'MFCD00053297',
    #          'source_url': 'https://search.otavachemicals.com/#!/compound/609a502cf1270034218f8004',
    #          'companyname': 'OTAVAchemicals', 'create_time': '2023-06-25 14:26:48',
    #          'update_time': '2023-06-25 14:26:48', 'spider': 'otava'}
    value = {'goods_id': 'AB118589-500 g', 'cas': '98-98-6', 'price': '€124.00', 'purity': '99%', 'productname': '2-Picolinic acid, 99%; .', 'specs': '500 g', 'mdl': 'MFCD00006293', 'stock': '', 'source_url': 'https://abcr.com/de_en/ab118589', 'source': 'abcr', 'companyname': 'abcr', 'create_time': '2023-08-28 15:38:50', 'update_time': '2023-08-28 15:38:50', 'spider': 'abc'}


    # kjutils().filter_lower(value=value)
    ff = Kjutils(string=value).process_item()
    pprint(ff)
