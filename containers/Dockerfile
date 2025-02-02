FROM python:3.9.11

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

# apt-getでsqlite3をインストール（Debian/Ubuntuベースの場合）
RUN apt-get update && apt-get install -y sqlite3

# requirements.txt をコピーしてパッケージをインストール
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# プロジェクト全体をコンテナにコピー
COPY . /app/

# 必要なポートを開放
EXPOSE 8000

# コンテナ起動時に実行するコマンドを指定
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
