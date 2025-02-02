FROM node:latest

# 作業ディレクトリの作成
WORKDIR /app

# package.json と package-lock.json をコピーして依存パッケージをインストール
COPY . .
RUN npm install
RUN npm install react-scripts

# アプリケーション全体をコピー
COPY . .

# ビルド（開発環境の場合はnpm startなど）
CMD ["npm", "start"]

EXPOSE 3000
