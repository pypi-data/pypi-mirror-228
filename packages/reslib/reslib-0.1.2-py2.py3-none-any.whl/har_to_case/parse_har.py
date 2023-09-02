# 导入yaml和其他需要的库
import json
import time
import sys

import yaml
import re
from haralyzer import HarParser
from loguru import logger

from har_to_case.common.tools import dump_yaml

logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
handler_id = logger.add(sys.stderr, level="INFO")  # 添加一个可以修改控制的handler


class ParseHar:
    regex_resource = re.compile(r"\/[^\/?\/]*\.(css|ico|jpg|png|gif|bmp|wav|js|jpeg|woff2)(\?.*)?")
    regex_name = re.compile(r"(?<=/api\/)(.*)(?=\?)|(?<=/api\/)(.*)")
    regex_api = re.compile(r"(\/api\/.*)")

    def __init__(self, har_file_path, output_file_path):
        '''
        ParseHar初始化，传入har文件路径，与输出文件路径
        :param har_file_path: har文件路径
        :param output_file_path: 输出文件路径
        '''
        with open(har_file_path, "r", encoding="utf-8") as f:
            self.har_parser = HarParser(yaml.safe_load(f))
        self.output_file_path = output_file_path

    def _make_request_name(self, entry: dict, test_case_dict: dict):
        '''
        解析har文件中entry项拼接出用例名，实际上是通过解析url后替换”/“为”-“生成用例名
        :param entry: har文件中entry项
        :return: 根据url拼接用例名
        '''
        global names
        if self.regex_resource.search(entry["request"]["url"]) is None:
            # 通过正则匹配url中的接口地址来取名
            names = self.regex_name.findall(entry["request"]["url"])
            try:
                for i in names[0]:
                    if i != '':
                        name = i.replace("/", '-')
                        test_case_dict['name'] = name
                        logger.info(f'成功解析用例名:{name}')
            except IndexError as e:
                logger.debug(e)
                logger.debug(names)
                pass

    def _make_request_url(self, entry: dict, request_dict: dict):
        '''
        解析har文件获取接口请求地址
        :param entry: har文件得entry部分
        :param request_dict: 构造的request字典
        :return:
        '''
        url = self.regex_api.findall(entry["request"]["url"])
        try:
            request_dict['url'] = url[0]
            logger.info(f'成功解析请求地址:{url[0]}')
        except IndexError as e:
            logger.debug(e)
            logger.debug(url)
            pass

    def _make_request_method(self, entry: dict, request_dict: dict):
        '''
        解析har文件获取请求方法
        :param entry: har文件得entry部分
        :param request_dict: 构造的request字典
        :return:
        '''
        request_dict['method'] = entry["request"]["method"]
        logger.info(f"成功解析请求方法:{request_dict['method']}")

    def _make_request_header(self, request_dict: dict):
        '''
        构造request字典中headers部分;框架中有独立的请求头生成方法,所以此工具只负责生成固定的请求头,不解析entry获取请求头信息
        :param request_dict:
        :return:
        '''

        request_dict['headers'] = {'Authorization': "", "Content-Type": "application/json; charset=utf-8"}
        logger.info(f"成功配置请求头:{request_dict['headers']}")

    def _make_request_params(self, entry: dict, request_dict: dict):
        '''
        解析har文件获取请求参数
        :param entry: har文件的entry部分
        :param request_dict: 构造的request字典
        :return:
        '''
        if "postData" in entry["request"]:
            request_dict['params'] = json.loads(entry["request"]["postData"]["text"])
            logger.info(f"成功解析请求参数:{request_dict['params']}")
        else:
            request_dict['params'] = None

    def _make_respone_validate(self, entry: dict, request_dict: dict):
        '''
        解析har文件respone部分,生成用例断言
        :param entry: har文件的entry部分
        :param request_dict: 构造的request字典
        '''
        try:
            data = json.loads(entry['response']['content']['text'])
            request_dict['validate']['equals']['status_code'] = data['status_code']
            logger.info(f"成功解析返回状态码:{request_dict['validate']['equals']}")
        except KeyError as e:
            logger.debug(e)

    def _make_respone_valiade_contains(self, entry: dict, request_dict: dict):
        '''
        解析har文件respone部分,通过返回体中的key生成断言应包含的关键字
        :param entry: har文件的entry部分
        :param request_dict: 构造的request字典
        :return:
        '''
        try:
            data = json.loads(entry['response']['content']['text'])
            data = data['data']
            validate_contains = ''
            if isinstance(data, dict):
                if len(data.keys()) <= 1:
                    validate_contains = 'data'
                else:
                    for key in data.keys():
                        if validate_contains == '':
                            validate_contains = key
                        else:
                            validate_contains = validate_contains + '-' + key
            else:
                for item in data:
                    # todo: data中的data继续解析，后续看需求再定
                    if isinstance(item, dict):
                        pass
                    else:
                        if validate_contains == '':
                            validate_contains = item
                        else:
                            logger.debug(item)
                            validate_contains = validate_contains + '-' + item
            request_dict['validate']['contains'] = validate_contains
            logger.info('成功解析返回体')
        except KeyError as e:
            logger.debug(e)

    def _generate_case_dict(self, entry, test_case_dict, request_dict):
        '''
        生成用例字典的函数,将
        :param entry:
        :param test_case_dict:
        :param request_dict:
        :return:
        '''
        self._make_request_name(entry, test_case_dict)
        self._make_request_url(entry, request_dict)
        self._make_request_method(entry, request_dict)
        self._make_request_params(entry, request_dict)
        self._make_request_header(request_dict)
        self._make_respone_validate(entry, request_dict)
        self._make_respone_valiade_contains(entry, request_dict)

    def _generate_case_list(self) -> list:
        # 遍历har文件中的每个请求
        test_case_list = []
        for page in self.har_parser.pages:
            for entry in page.entries:
                # 提取需要的信息
                if self.regex_resource.search(entry["request"]["url"]) is None:
                    request_dict = {
                        "url": '',
                        "method": '',
                        "headers": '',
                        # "cookies": cookies,
                        "params": '',
                        "validate": {
                            'equals': {
                                'status_code': ''
                            },
                            'contains': ''
                        }
                    }
                    test_case_dict = {"name": '',
                                      "requests": request_dict}
                    # 构建框架用例格式字典
                    logger.info(
                        '---------------------------------------构建用例--------------------- -----------------')
                    self._generate_case_dict(entry, test_case_dict, request_dict)
                    if test_case_dict['name'] == '':
                        pass
                    else:
                        test_case_list.append(test_case_dict)
            return test_case_list

    def generate_yaml_case(self):
        '''
        生成yaml格式用例
        '''
        now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        if '.yaml' in self.output_file_path or '.yml' in self.output_file_path:
            file = self.output_file_path

        else:
            file = self.output_file_path + f"/record_{now}.yaml"
        test_case = self._generate_case_list()
        dump_yaml(test_case, file)


if __name__ == '__main__':
    case = ParseHar('./192.168.1.117.har', './casefile')
    case.generate_yaml_case()
