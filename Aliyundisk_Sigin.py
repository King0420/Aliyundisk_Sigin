import json
import requests
import time

class SignIn:
    """
    签到
    """

    def __init__(self, refresh_token: str):
        """
        初始化

        :param refresh_token: refresh_token
        """
        self.refresh_token = refresh_token
        self.access_token = None
        self.new_refresh_token = None
        self.phone = None
        self.signin_count = 0
        self.signin_reward = None
        self.error = None

    def __get_access_token(self) -> bool:
        """
        获取 access_token

        :return: 是否成功
        """
        try:
            data = requests.post(
                'https://auth.aliyundrive.com/v2/account/token',
                json={
                    'grant_type': 'refresh_token',
                    'refresh_token': self.refresh_token,
                }
            ).json()
        except requests.RequestException as e:
            self.error = e
            return False

        try:
            self.access_token = data['access_token']
            self.new_refresh_token = data['refresh_token']
            self.phone = data['user_name']
        except KeyError:
            self.error = f'获取 access token 失败, 参数缺失: {data}'
            return False

        return True

    def __sign_in(self) -> None:
        """
        签到函数

        :return:
        """
        try:
            data = requests.post(
                'https://member.aliyundrive.com/v1/activity/sign_in_list',
                params={'_rx-s': 'mobile'},
                headers={'Authorization': f'Bearer {self.access_token}'},
                json={'isReward': False},
            ).json()
        except requests.RequestException as e:
            self.error = e
            return

        self.signin_count = data['result']['signInCount']

        try:
            data = requests.post(
                'https://member.aliyundrive.com/v1/activity/sign_in_reward',
                params={'_rx-s': 'mobile'},
                headers={'Authorization': f'Bearer {self.access_token}'},
                json={'signInDay': self.signin_count},
            ).json()
        except requests.RequestException as e:
            self.error = e
            return

        reward = (
            '无奖励'
            if not data['result']
            else f'获得 {data["result"]["name"]} {data["result"]["description"]}'
        )

        self.signin_reward = reward

        print(f'签到成功, 本月累计签到 {self.signin_count} 天.')
        print(f'本次签到{reward}')

    def run(self) -> None:
        """
        运行签到

        :return:
        """
        if self.__get_access_token():
            time.sleep(3)
            self.__sign_in()

# 在下面填写你的 refresh_token
refresh_token = "your_refresh_token"
signin = SignIn(refresh_token=refresh_token)
signin.run()
