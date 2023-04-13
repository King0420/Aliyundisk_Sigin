# 阿里云盘签到

> 获取refresh_token地址：https://alist.nn.ci/zh/guide/drivers/aliyundrive.html

![image](https://user-images.githubusercontent.com/104044278/231685287-b4ef9f0c-de22-42cb-8065-6dc088bdb9fa.png)

替换Aliyundisk_Sigin.py中的**your_refresh_token**，部署在服务器中每天运行即可签到。

可以在宝塔面板中运行
```bash
cd /www/wwwroot 
export PYTHONIOENCODING=UTF-8
python3 Aliyundisk_Sigin.py
```
![image](https://user-images.githubusercontent.com/104044278/231066081-98ce07c5-4480-47a0-b6ba-f0bdbc95e304.png)
