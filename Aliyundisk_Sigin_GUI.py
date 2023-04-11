import json
import requests
import time
import tkinter as tk
from tkinter import messagebox


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
                }).json()
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
                params={
                    '_rx-s': 'mobile'
                },
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                },
                json={
                    'isReward': False
                },
            ).json()
        except requests.RequestException as e:
            self.error = e
            return

        self.signin_count = data['result']['signInCount']

        try:
            data = requests.post(
                'https://member.aliyundrive.com/v1/activity/sign_in_reward',
                params={
                    '_rx-s': 'mobile'
                },
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                },
                json={
                    'signInDay': self.signin_count
                },
            ).json()
        except requests.RequestException as e:
            self.error = e
            return

        reward = (
            '无奖励' if not data['result'] else
            f'获得 {data["result"]["name"]} {data["result"]["description"]}')

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


class SignInGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("签到程序")
        self.root.geometry("400x200")

        self.title_label = tk.Label(self.root,
                                    text="阿里云盘签到",
                                    font=("Arial", 16))
        self.title_label.pack(pady=10)

        self.refresh_token_label = tk.Label(self.root, text="Refresh Token:")
        self.refresh_token_label.pack()

        self.refresh_token_entry = tk.Entry(self.root)
        self.refresh_token_entry.pack(pady=5)

        self.sign_in_button = tk.Button(self.root,
                                        text="签到",
                                        command=self.sign_in)
        self.sign_in_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=5)

        self.root.mainloop()

    def sign_in(self):
        refresh_token = self.refresh_token_entry.get()

        if not refresh_token:
            messagebox.showerror("错误", "请输入 Refresh Token")
            return

        signin = SignIn(refresh_token=refresh_token)
        signin.run()

        if signin.error:
            messagebox.showerror("错误", f"签到失败：{signin.error}")
        else:
            result = (f"签到成功, 本月累计签到 {signin.signin_count} 天.\n"
                      f"本次签到{signin.signin_reward}")
            self.result_label.config(text=result)
            
if __name__ == "__main__":
    SignInGUI()
