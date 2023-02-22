* 启动程序： `app.py`
* uwsgi启动： `uwsgi -d --ini app.ini`
* 目录树：
  * controller：路由分发
  * module：逻辑处理
  * query：对象交互