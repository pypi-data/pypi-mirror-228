import unittest
import sys
from parameterized import parameterized

from st_common import CommonBase



class CommonBaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print("在每个类之前执行，如创建一个类，创建数据库链接，初始化日志对象")
        cls.commonbase = CommonBase()
    @classmethod
    def tearDownClass(cls) -> None:
        print("在每个类之后执行，如销毁一个类，销毁数据库链接，销毁日志对象")
        pass

    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    @parameterized.expand([
        (1123,False),("asdf",False),("123asdf",False),
        ("你好",True),("你好，world",True)
        ])
    def test_is_contains_chinese(self,strs, result):
        self.assertEqual(first=self.commonbase._is_contains_chinese(strs=strs),second=result)
    
    
