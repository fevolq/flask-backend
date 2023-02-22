# 镜像基础
FROM python:3.7

# 复制当前代码文件到容器中
ADD . /app

# 设置代码文件夹工作目录
WORKDIR /app

# 安装依赖
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple

# 执行项目
CMD ["python", "main.py"]
