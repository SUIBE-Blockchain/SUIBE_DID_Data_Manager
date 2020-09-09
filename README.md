# SUIBE_DID_Data_Manager
上贸大去中心化数字身份管理工具（网页端）

## 运行 SUIBE DID Data Manager

**运行环境**

python3.7+

**运行 SUIBE DID Data Manager**

~~~bash
git clone git@github.com:SUIBE-Blockchain/SUIBE_DID_Data_Manager.git

cd SUIBE_DID_Data_Manager/

mv .envrc SUIBE_DID_Data_Manager/.env

pip install -r requirements.txt

python manager.py init_db
# init db
python manager.py runserver 
# 运行服务
~~~



-----------------



**\* manager.py 启动脚本命令**

~~~bash
python manager.py init_db
# init db
python manager.py reset_db
# reset db
python manager.py set_user <username> <email> <password> <active>
# add user
python manger.py runserver 
# 运行服务
~~~

