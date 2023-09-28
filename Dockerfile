#基础镜像
FROM python:3

#将当前目录中的文件加入到镜像中的/app目录下
ADD . /app

#设置工作目录为/app
WORKDIR /app

#安装requirements.txt中列举的包
RUN pip install --trusted-host pypi.python.org -r requirements.txt

#对外暴露端口
EXPOSE 80

#设置环境变量
ENV NAME World

#在容器启动时运行app.py
CMD ["python", "app.py"]
