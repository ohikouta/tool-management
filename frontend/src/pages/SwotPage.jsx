// src/pages/SwotPage.jsx
import React, { useState, useEffect } from 'react';
import SWOTForm from '../components/SwotForm'; // SWOTForm.jsxはフォームコンポーネントとして別途実装している前提

const SwotPage = () => {
  const [analysis, setAnalysis] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // バックエンドからSWOT分析一覧を取得する関数（fetchを使用）
  const fetchAnalysis = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/swot-analysis/',{
        credentials: 'include'
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      console.error('データ取得エラー:', err);
      setError('データの取得に失敗しました。');
    }
    setLoading(false);
  };

  // コンポーネントのマウント時に一覧を取得
  useEffect(() => {
    fetchAnalysis();
  }, []);

  // SWOTFormから新規作成時のコールバックを受け取る
  const handleSWOTCreated = (newAnalysis) => {
    setAnalysis((prev) => [...prev, newAnalysis]);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>SWOT 分析</h1>
      {/* SWOTFormコンポーネントは、送信成功時に onSuccess コールバックで新規作成データを返すよう実装してください */}
      <SWOTForm onSuccess={handleSWOTCreated} />
      <hr />
      <h2>過去の分析一覧</h2>
      {loading && <p>読み込み中...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {!loading && analysis.length === 0 ? (
        <p>まだ分析がありません。</p>
      ) : (
        <ul>
          {analysis.map((analysis) => (
            <li key={analysis.id} style={{ marginBottom: '15px' }}>
              <h3>{analysis.title}</h3>
              <p>作成日時: {new Date(analysis.created_at).toLocaleString()}</p>
              {analysis.items && analysis.items.length > 0 ? (
                <ul>
                  {analysis.items.map((item) => (
                    <li key={item.id}>
                      <strong>{item.category}:</strong> {item.content}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>アイテムがありません。</p>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SwotPage;
