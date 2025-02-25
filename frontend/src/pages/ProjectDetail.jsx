import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import InviteMember from './projects/InviteMember';
import ChatComponent from './projects/ChatComponent';
// 既存のSWOT, クロスSWOTのフォームはここでは表示せず、SWOT編集ページへ遷移する導線を追加する
// import SWOTForm from '../components/SwotForm';
// import CrossSwotForm from '../components/CrossSwotForm';

function ProjectDetail() {
  const { id } = useParams();   // ルートパラメータからidを取得
  const [project, setProject] = useState(null);

  const getCsrfToken = () => {
    const match = document.cookie.match(/csrftoken=([\w-]+)/);
    return match ? match[1] : null;
  };

  useEffect(() => {
    const csrfToken = getCsrfToken();

    // 例: Django REST Frameworkのエンドポイントが /api/projects/:id の場合
    fetch(`http://localhost:8000/api/projects/${id}/`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      }
    })
      .then(response => response.json())
      .then(data => setProject(data))
      .catch(error => console.error('Error fetching project:', error));
  }, [id]);

  if (!project) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h2>プロジェクト詳細</h2>
      <p>プロジェクト名: {project.name}</p>
      <p>開始日: {project.start_date}</p>
      <h3>クライアント概要</h3>
      <p>商店街の人通りが非常に少なくなっている。商店街全体のプロモーションを見直して、復興していきたい。</p>
      <h3>プロジェクトメンバー</h3>
      {project.members && project.members.length > 0 ? (
        <ul>
          {project.members.map(member => (
            <li key={member.id}>{member.username}</li>
          ))}
        </ul>
      ) : (
        <p>メンバーはいません</p>
      )}
      <p>メンバーを追加</p>
      <InviteMember projectId={id} />

      <h3>SWOT分析</h3>
      {/* SWOT編集ページへのリンクを追加 */}
      {project.swot_analysis && project.swot_analysis.length > 0 ? (
        <ul>
          {project.swot_analysis.map(swot => (
            <li key={swot.id}>
              <Link to={`/projects/${project.id}/swot-edit/${swot.id}`}>
                {swot.title || '無題のSWOT分析'}
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>このプロジェクトにはまだ SWOT 分析が作成されていません。<Link to={`/projects/${project.id}/swot-edit/`}>新規作成する</Link></p>
      )}


      <h3>チャット</h3>
      <ChatComponent roomId={project.id} />
    </div>
  );
}

export default ProjectDetail;
