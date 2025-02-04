// frontend/src/components/Home.jsx
import React from "react";
import { Link } from "react-router-dom";
import "./Home.css"; // 同じフォルダにHome.cssを用意する想定

const Home = () => {
  console.log("Homeコンポーネントがレンダリングされました");
  return (
    <div className="home-container">
      <h1 className="home-title">ようこそ！</h1>
      <p className="home-description">
        ログインするか、新規アカウントを作成してください。
      </p>
      <div className="home-buttons">
        <Link to="/login" className="home-button login-button">
          ログイン
        </Link>
        <Link to="/signup" className="home-button signup-button">
          新規登録
        </Link>
      </div>
    </div>
  );
};

export default Home;
