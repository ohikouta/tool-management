# Pythonイメージをベースにする
FROM python:3.9.11

# 環境変数（出力をバッファリングしない）
ENV PYTHONUNBUFFERED 1

# --- ここを追加 ---
# apt-get update & install で sqlite3をインストール
RUN apt-get update && apt-get install -y sqlite3

# 作業ディレクトリを作成
RUN mkdir -p /app
WORKDIR /app

# requirements.txt をコピーしてパッケージをインストール
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# プロジェクト全体を /app にコピー
COPY . /app/

# ポート開放
EXPOSE 8000

# コンテナ起動時のコマンド（manage.py は src/直下にある）
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
