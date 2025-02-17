// src/components/Header.jsx
import React, { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { Link } from 'react-router-dom';

const Header = () => {
  const { user, logout } = useContext(AuthContext);

  const handleLogout = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/auth/logout/', {
        method: 'POST',
        credentials: 'include',
      });
      if (response.ok) {
        logout();
      }
    } catch (error) {
      console.error('ログアウトエラー:', error);
    }
  };

  return (
    <header style={{ padding: '10px', borderBottom: '1px solid #ccc' }}>
      <h1>中小企業診断士ツールサイト</h1>
      {user ? (
        <div>
          <span>ログイン中: {user.username}</span>
          <button onClick={handleLogout}>ログアウト</button>
        </div>
      ) : (
        <div>
          <Link to="/login">ログイン</Link>
        </div>
      )}
    </header>
  );
};

export default Header;
