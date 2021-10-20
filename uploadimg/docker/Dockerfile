FROM python:3.6

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ flask requests --upgrade

USER root
RUN useradd app
RUN mkdir /app && chown app:app /app
COPY app/localtime /etc/localtime
ENV LANG en_US.UTF-8
USER app
ADD app/app.tar.gz /app/
WORKDIR /app
EXPOSE 8080
CMD python3.5 server.py