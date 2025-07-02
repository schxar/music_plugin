import http.client
import json

class NapcatClient:
    def __init__(self, host="127.0.0.1", port=4998):
        self.host = host
        self.port = port

    def send_group_music_card(self, group_id: int, music_type: str, music_id: str):
        """
        发送音乐小程序卡片到指定群聊。
        :param group_id: 群号
        :param music_type: 音乐平台类型（如 '163'）
        :param music_id: 音乐ID
        :return: Napcat响应内容
        """
        conn = http.client.HTTPConnection(self.host, self.port)
        payload = json.dumps({
            "group_id": group_id,
            "message": [
                {
                    "type": "music",
                    "data": {
                        "type": music_type,
                        "id": music_id
                    }
                }
            ]
        })
        headers = {'Content-Type': 'application/json'}
        conn.request("POST", "/send_group_msg", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

    def send_group_record(self, group_id: int, file_path: str):
        """
        发送语音消息到指定群聊。
        :param group_id: 群号
        :param file_path: 语音文件路径（本地或网络）
        :return: Napcat响应内容
        """
        conn = http.client.HTTPConnection(self.host, self.port)
        payload = json.dumps({
            "group_id": group_id,
            "message": [
                {
                    "type": "record",
                    "data": {
                        "file": file_path
                    }
                }
            ]
        })
        headers = {'Content-Type': 'application/json'}
        conn.request("POST", "/send_group_msg", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

    def send_private_music_card(self, user_id: int, music_type: str, music_id: str):
        """
        发送音乐小程序卡片到指定私聊。
        :param user_id: 用户ID
        :param music_type: 音乐平台类型（如 '163'）
        :param music_id: 音乐ID
        :return: Napcat响应内容
        """
        conn = http.client.HTTPConnection(self.host, self.port)
        payload = json.dumps({
            "user_id": user_id,
            "message": [
                {
                    "type": "music",
                    "data": {
                        "type": music_type,
                        "id": music_id
                    }
                }
            ]
        })
        headers = {'Content-Type': 'application/json'}
        conn.request("POST", "/send_private_msg", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

    def send_private_record(self, user_id: int, file_path: str):
        """
        发送语音消息到指定私聊。
        :param user_id: 用户ID
        :param file_path: 语音文件路径（本地或网络）
        :return: Napcat响应内容
        """
        conn = http.client.HTTPConnection(self.host, self.port)
        payload = json.dumps({
            "user_id": user_id,
            "message": [
                {
                    "type": "record",
                    "data": {
                        "file": file_path
                    }
                }
            ]
        })
        headers = {'Content-Type': 'application/json'}
        conn.request("POST", "/send_private_msg", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")
