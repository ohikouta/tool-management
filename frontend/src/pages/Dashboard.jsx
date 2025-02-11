import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import LogoutButton from '../components/LogoutButton';

function Dashboard() {
  useEffect(() => {
    // CSRFトークンセット用エンドポイントにアクセス
    fetch('http://localhost:8000/api/csrf/', {
      method: 'GET',
      credentials: 'include'
    })
      .then(response => response.json())
      .then(data => {
        console.log('CSRF cookie set:', data);
      })
      .catch(error => {
        console.error('CSRF cookie取得エラー:', error);
      });
  }, []);

  return (
    <div>
      <LogoutButton />
      <div>
        <h2>プロジェクト</h2>
      </div>
      <h2>基礎知識</h2>
      <nav>
      <h2>1次試験7科目</h2>
        <ul>
          <h2>経済学・経済政策</h2>
          <li><Link to="/swot">SWOT 作成ページ</Link></li>
          <li><Link to="/4p">4P 作成ページ</Link></li>
        </ul>
        <ul>
          <h2>財務・会計</h2>
          <li><Link to="/swot">BS/PLのコツ</Link></li>
          <li><Link to="/4p"></Link></li>
        </ul>
        <ul>
          <h2>企業経営理論</h2>
          <li><Link to="/swot">SWOT 作成ページ</Link></li>
          <li><Link to="/4p">4P 作成ページ</Link></li>
        </ul>
        <ul>
          <h2>運営管理（オペレーション・マネジメント）</h2>
          <li><Link to="/swot">SWOT 作成ページ</Link></li>
          <li><Link to="/4p">4P 作成ページ</Link></li>
        </ul>
        <ul>
          <h2>経営法務</h2>
          <li><Link to="/swot">SWOT 作成ページ</Link></li>
          <li><Link to="/4p">4P 作成ページ</Link></li>
        </ul>
        <ul>
          <h2>経営情報システム</h2>
          <li><Link to="/swot">SWOT 作成ページ</Link></li>
          <li><Link to="/4p">4P 作成ページ</Link></li>
        </ul>
        <ul>
          <h2>中小企業経営・政策</h2>
          <li><Link to="/swot">SWOT 作成ページ</Link></li>
          <li><Link to="/4p">4P 作成ページ</Link></li>
        </ul>
      <h2>2次試験事例</h2>
      </nav>
    </div>
  );
}

export default Dashboard;
