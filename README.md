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

python manager.py init_local_db
# init local db

python manager.py runserver 
# 运行服务
~~~
-----------------


~~~bash
positional arguments:
  {runserver,shell,reset_local_db,reset_server_db,reset_db,init_local_db,init_server_db,init_db,set_user}
    runserver           Runs the Flask development server i.e. app.run()
    shell               Runs a Python shell inside Flask application context.
    reset_local_db      Reset local databases.
    reset_server_db     Reset server databases.
    reset_db            Reset all databases.
    init_local_db       Initialized local databases.
    init_server_db      Initialized server databases.
    init_db             Initialized all databases.
    set_user            Add A New User.
~~~

