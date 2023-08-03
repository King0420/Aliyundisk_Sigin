# 阿里云盘自动签到
![Aliyundisk_Sigin](https://socialify.git.ci/King0420/Aliyundisk_Sigin/image?description=1&font=Inter&forks=1&language=1&name=1&owner=1&stargazers=1&theme=Light)
1
**一、获取refresh_token地址**：https://alist.nn.ci/zh/guide/drivers/aliyundrive.html

![image](https://user-images.githubusercontent.com/104044278/231685287-b4ef9f0c-de22-42cb-8065-6dc088bdb9fa.png)

**二、替换Aliyundisk_Sigin.py中的your_refresh_token，部署在服务器中每天运行即可签到。**
![image](https://user-images.githubusercontent.com/104044278/231686151-d96fccb9-9dcf-414a-8f0a-b3a37fb56cb7.png)

**三、可以在宝塔面板中每天运行**
```bash
cd /www/wwwroot 
export PYTHONIOENCODING=UTF-8
python3 Aliyundisk_Sigin.py
```
![image](https://user-images.githubusercontent.com/104044278/231066081-98ce07c5-4480-47a0-b6ba-f0bdbc95e304.png)
