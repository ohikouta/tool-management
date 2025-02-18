import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

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
      {/* 他に必要な情報があれば追加 */}
    </div>
  );
}

export default ProjectDetail;
