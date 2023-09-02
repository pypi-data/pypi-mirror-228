import base64
import os

import requests
import yantu


class YantuObject:
    BASE_URL = 'http://localhost:8555/api/v1/'

    # BASE_URL = 'http://www.yantu-tech.com/api/v1'

    def __init__(self, yantu_key):
        self.yantu_key = yantu_key

    def _make_request(self, endpoint, data):
        """
        执行请求
        :param endpoint:
        :param data:
        :return:
        """
        url = self.BASE_URL + endpoint
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response

    def upload_doc(self, doc_path):
        """
        私域知识库文档上传
        :param doc_path: 文档路径
        :return:
        """
        data = {
            'yantu_key': self.yantu_key,
            'doc': base64.b64encode(open(doc_path, 'rb').read()).decode('utf-8'),
            'doc_name': os.path.basename(doc_path)
        }
        response = self._make_request('uploadDoc', data)
        open(doc_path, 'rb').close()  # 关闭文件
        return response.text

    def get_doc_list(self):
        """
        获取私域知识库文档列表
        :return:
        """
        data = {
            'yantu_key': self.yantu_key
        }
        response = self._make_request('getDocList', data)
        json_res = response.json()
        if 'doc_list' in json_res:
            return json_res['doc_list']
        else:
            return json_res['res']

    def delete_doc(self, filename):
        """
        删除私域知识库中文档
        :param filename: 文档名称
        :return:
        """
        data = {
            'yantu_key': self.yantu_key,
            'filename': filename
        }
        response = self._make_request('deleteDoc', data)
        return response.text

    def doc_qa(self, question):
        """
        基于私域知识库中内容进行文档问答
        :param question:
        :return:
        """
        data = {
            'yantu_key': self.yantu_key,
            'question': question
        }
        response = self._make_request('docQA', data)
        answer = response.text
        return answer


if __name__ == '__main__':
    yt_object = YantuObject('yt-92D7e51Ec069469a8')
    print(yt_object.get_doc_list())
    # print(yt_object.upload_doc('../CPCR技术文档.doc'))
    # print(yt_object.delete_doc('CPCR技术文档.doc'))
    # print(yt_object.doc_qa('患者情况的评估条件有哪些'))
    # print(yt_object.doc_qa('心肺复苏术是什么'))
