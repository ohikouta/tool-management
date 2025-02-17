import React, { useState } from 'react';

const formStyle = {
    width: '700px'
}

const labelStyle = {
    display: 'block',
    marginBottom: '5px'
}

const inputStyle = {
    width: '300px',
    height: '30px',
    marginBottom: '15px',
}

const inputTitleStyle = {
    width: '500px',
    height: '30px',
    marginBottom: '15px',
}

const ProjectForm = ({ onSuccess, initialData = {} }) => {
  const [year, setYear] = useState(initialData.year || '');
  const [startDate, setStartDate] = useState(initialData.start_date || '');
  const [name, setName] = useState(initialData.name || '');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = { year, start_date: startDate, name };
    try {
      const getCsrfToken = () => {
        const match = document.cookie.match(/csrftoken=([\w-]+)/);
        return match ? match[1] : null;
      };
      const csrfToken = getCsrfToken();
      const response = await fetch('http://localhost:8000/api/projects/', {
        method: initialData.id ? 'PUT' : 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        throw new Error('プロジェクトの保存に失敗しました');
      }
      const responseData = await response.json();
      console.log('保存成功:', responseData);
      if (onSuccess) {
        onSuccess(responseData);
      }
    } catch (error) {
      console.error('保存エラー:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div style={formStyle}>
        <label style={labelStyle}>開始日:</label>
        <input style={inputStyle} type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
      </div>
      <div>
        <label style={labelStyle}>プロジェクト名:</label>
        <input style={inputTitleStyle} type="text" value={name} onChange={(e) => setName(e.target.value)} />
      </div>
      <button type="submit">{initialData.id ? '更新' : '保存'}</button>
    </form>
  );
};

export default ProjectForm;
