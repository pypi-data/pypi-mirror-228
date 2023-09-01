# -*- coding: utf-8 -*- 
# @Time : 2023/8/17 下午3:20
# @Author : zhaomeng
# @File : PriceStock.py
# @desc:
import logging
import traceback
import pymssql
from dbutils.pooled_db import PooledDB

from kjutils.kjutils import Kjutils


class PriceStockPipeline:
    def __init__(self, settings: dict = None):
        # 建立连接
        self.server = settings.get("server")
        self.port = settings.get("port")
        self.user = settings.get("user")
        self.password = settings.get("password")
        self.database = settings.get("database")
        # 建立连接
        pool = PooledDB(creator=pymssql, mincached=2, maxcached=5, maxshared=3, maxconnections=6, blocking=True,
                        host=self.server, port=self.port, user=self.user, password=self.password,
                        database=self.database, charset="utf8")
        self.connect = pool.connection()

        self.cursor = self.connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行

    def select_exist(self, content: dict):
        """
         判断数据是否存在
        :param content:
        :param sql:  查询语句
        :return:
        """
        info = content
        sql = f"select Id from ChemPriceList where IsDeleted=0 AND ProductNo=%s AND SourceUrl=%s"
        param = (info.get('ProductNo'), info.get('SourceUrl'))
        self.cursor.execute(sql, param)  # 执行sql语句
        if self.cursor.fetchone():
            # print(self.cursor.fetchone())
            return True
        else:
            return False
        pass

    def specs_exist(self, content: dict):
        """
         判断规格数据是否存在
        :param content:
        :param sql:  查询语句
        :return:
        """
        info = content
        sql = f"select Id from SpecList where Specification=%s"
        param = (info.get('Specification'),)
        self.cursor.execute(sql, param)  # 执行sql语句
        if self.cursor.fetchone():
            return True
        else:
            return False

    def update(self, content: dict):
        """
        数据据存在就更新
        :param content:
        :param sql:
        :return:
        """
        info = content
        sql = f"""    
               update ChemPriceList set 
               ProductName=%s,
               CasNo=%s,
               Purity=%s,
               Specification=%s,
               Price=%s,
               InStock=%s,
               CompanyName=%s,
               Souce=%s,
               Mdl=%s,
               SourceUrl=%s,
               LastModificationTime=%s where IsDeleted=0 AND ProductNo=%s AND SourceUrl=%s
               """
        param = (info.get('ProductName', ''), info.get('CasNo'), info.get('Purity', ''), info.get('Specification'),
                 info.get('Price'), info.get('InStock', ''), info.get('CompanyName'),
                 info.get('Souce'), info.get("Mdl", ''), info.get('SourceUrl'), info.get('LastModificationTime'),
                 info.get('ProductNo'),
                 info.get('SourceUrl'))
        try:
            print(info.get('ProductNo'), info.get('SourceUrl'))
            self.cursor.execute(sql, param)
            self.connect.commit()
        except Exception as e:
            print(e)
            logging.error(traceback.print_exc())
            self.connect.rollback()

        pass

    def insert(self, content: dict):
        """
        插入数据
        :param content:
        :param info:
        :return:
        """
        info = content
        # print(info)

        add_sql = f"""
                    INSERT INTO ChemPriceList (
                            ProductNo,
                            ProductName,
                            CasNo,
                            Purity,
                            Specification,
                            Price,
                            InStock,
                            CompanyName,
                            Souce,
                            Mdl,
                            SourceUrl,
                            CheckStatus,
                            IsActive,
                            Remark,
                            TenantId,
                            CreationTime,
                            IsDeleted)
                            VALUES(%s, 
                                    %s, 
                                    %s, 
                                    %s, 
                                    %s, 
                                    %s, 
                                    %s, 
                                    %s, 
                                    %s, 
                                    %s, 
                                    %s, 
                                    %s,
                                    %s,
                                    %s, 
                                    %s, 
                                    %s, 
                                    %s) 
                """

        try:
            param = (info.get('ProductNo'), info.get('ProductName', ''), info.get('CasNo'), info.get('Purity', ''),
                     info.get('Specification'), info.get('Price'), info.get('InStock', ''), info.get('CompanyName'),
                     info.get('Souce'), info.get("Mdl", ''), info.get('SourceUrl'), 1, 1, '采集同步', 1,
                     info.get('CreationTime'), 0)
            self.cursor.execute(add_sql, param)
            self.connect.commit()
        except Exception as e:
            print(e)
            logging.error(traceback.print_exc())
            self.connect.rollback()

    def delete(self, info):
        """
        删除数据
        :param info:
        :return:
        """
        sql = f"DELETE ChemPriceList WHERE SourceUrl={repr(info.get('source_url'))}"
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            # print(sql)

        except Exception as e:
            print(e)
            logging.error(traceback.print_exc())
            self.connect.rollback()

    def process_item(self, item):
        try:
            content = dict(item)

            result = Kjutils(string=content).process_item()
            info = {
                "ProductNo": result.get('goods_id'),
                "ProductName": result.get('productname', ''),
                "CasNo": result.get('cas').strip(),
                "Purity": result.get("purity") if result.get("purity") else '',
                "Specification": result.get('specs'),
                "Price": result.get('price'),
                "InStock": result.get("stock") if result.get("stock") else '',
                "CompanyName": result.get("companyname"),
                "Souce": result.get('source'),
                "Mdl": result.get("mdl", ''),
                "SourceUrl": result.get('source_url').strip(),
                "CreationTime": result.get('create_time'),
                'LastModificationTime': result.get("update_time")
            }
            if not self.specs_exist(content):
                spec_info = {
                    "Specification": content.get("specs"),
                    "DealSrcSpec": result.get("specs")
                }
                self.specs(info=spec_info)
            else:
                pass
            if self.select_exist(info):
                self.update(info)
                print(f"更新数据{info.get('ProductNo')}")
                logging.info(f"更新数据{info.get('ProductNo')}")

                pass
            else:
                self.insert(info)
                print(f"插入数据{info.get('ProductNo')}")
                logging.info(f"插入数据{info.get('ProductNo')}")

        except Exception as e:
            logging.error(traceback.print_exc())
            # exit()
        finally:
            self.close()

    def delete_404(self, info):
        """
        删除无效404链接
        :param info:
        :return:
        """
        if self.select_exist(info):
            self.delete(info)
            logging.info(f'删除404无效状态链接:{info.get("source_url")}')
        else:
            logging.info(f'无效状态链接:{info.get("source_url")}')

    def specs(self, info: dict):
        """
        获取规格数据，规格不存在就存入，存在不做处理
        :param info:
        :return:
        """
        if self.specs_exist(content=info):
            pass
        else:
            add_sql = f"""
                        INSERT INTO SpecList (
                                Specification,
                                DealSrcSpec,
                                CheckStatus,
                                SrcSpec
                                )
                                VALUES(%s, 
                                        %s, 
                                        %s, 
                                        %s
                                        ) 
                        """

            try:
                param = (info.get('Specification'), info.get('DealSrcSpec', ''), 0, info.get('DealSrcSpec', ''))
                self.cursor.execute(add_sql, param)
                self.connect.commit()
            except Exception as e:
                print(e)
                logging.error(traceback.print_exc())
                self.connect.rollback()

    def close(self):
        self.cursor.close()  # 关闭游标
        self.connect.close()  # 关闭连接


if __name__ == '__main__':
    pass
    # d={}
    # print(d)
    # d = Kjutils(string=d).process_item()
    # print(d)
    # F = PriceStockPipeline()
    # F.process_item(item=d)
