import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';

// ユーザーごとの色を決める関数例（簡単なハッシュからカラーを算出）
const getUserColor = (username) => {
  const colors = ['#FF5733', '#33C3FF', '#9D33FF', '#33FF57', '#FFC300'];
  let hash = 0;
  for (let i = 0; i < username.length; i++) {
    hash = username.charCodeAt(i) + ((hash << 5) - hash);
  }
  const index = Math.abs(hash) % colors.length;
  return colors[index];
};

function CollaborativeSwotEditor({ swotId, projectId, initialTitle, initialItems, onSave }) {
  const { user } = useContext(AuthContext);
  const [title, setTitle] = useState(initialTitle || '');
  const [items, setItems] = useState(
    initialItems || {
      Strength: [''],
      Weakness: [''],
      Opportunity: [''],
      Threat: ['']
    }
  );
  const [socket, setSocket] = useState(null);
  // 編集状態を管理する state。キーは「category-index」、値は { username, color }。
  const [editingState, setEditingState] = useState({});

  useEffect(() => {
    if (!user) return;
    const ws = new WebSocket(`ws://localhost:8000/ws/swot-collab/${swotId}/`);
    setSocket(ws);

    ws.onopen = () => {
      console.log("SwotCollab WebSocket connected");
      // オンライン通知
      ws.send(JSON.stringify({
        type: "online",
        username: user.username,
      }));
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      switch (data.type) {
        case "update_title":
          setTitle(data.title);
          break;
        case "update_item":
          setItems(prevItems => {
            const updated = { ...prevItems };
            if (updated[data.category]) {
              updated[data.category][data.index] = data.content;
            }
            return updated;
          });
          break;
        case "editing_field":
          // data は { type: "editing_field", category, index, username, status } 
          // status: "start" または "stop"
          const fieldKey = `${data.category}-${data.index}`;
          setEditingState(prev => {
            const newState = { ...prev };
            if (data.status === "start") {
              newState[fieldKey] = {
                username: data.username,
                color: data.color || getUserColor(data.username)
              };
            } else if (data.status === "stop") {
              delete newState[fieldKey];
            }
            return newState;
          });
          break;
        default:
          console.log("Unknown event type:", data.type);
      }
    };

    ws.onerror = (error) => {
      console.error("SwotCollab WebSocket error:", error);
    };

    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
          type: "offline",
          username: user.username,
        }));
      }
      ws.close();
    };
  }, [swotId, user]);

  // タイトル変更時にリアルタイム送信
  const handleTitleChange = (e) => {
    const newTitle = e.target.value;
    setTitle(newTitle);
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({
        type: "update_title",
        title: newTitle,
        username: user.username,
      }));
    }
  };

  // 各アイテム変更時のハンドラー
  const handleItemChange = (category, index, value) => {
    const updatedItems = { ...items };
    updatedItems[category][index] = value;
    setItems(updatedItems);
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({
        type: "update_item",
        category,
        index,
        content: value,
        username: user.username,
      }));
    }
  };

  // アイテム追加
  const handleAddItem = (category) => {
    const updatedItems = { ...items };
    updatedItems[category].push('');
    setItems(updatedItems);
  };

  // 編集開始（個々の入力フィールドで呼び出す）
  const startEditingField = (category, index) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      const fieldKey = `${category}-${index}`;
      const color = getUserColor(user.username);
      socket.send(JSON.stringify({
        type: "editing_field",
        category,
        index,
        username: user.username,
        status: "start",
        color: color,
      }));
    }
  };

  // 編集終了（個々の入力フィールドで呼び出す）
  const stopEditingField = (category, index) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({
        type: "editing_field",
        category,
        index,
        username: user.username,
        status: "stop",
      }));
    }
  };

  // 保存ボタンのハンドラー
  const handleSave = async () => {
    // itemsのオブジェクトからリスト形式に変換
    const transformedItems = [];
    for (const category in items) {
      items[category].forEach(content => {
        if (content.trim() !== '') {
          transformedItems.push({ category, content });
        }
      });
    }

    const payload = {
      title,
      items: transformedItems,
      project: projectId,
    };
    try {
      const csrfToken = document.cookie.match(/csrftoken=([\w-]+)/)[1];
      // swotId が定義されていれば更新用エンドポイント、未定義なら作成用エンドポイントを使用
      const endpoint = swotId 
        ? `http://localhost:8000/api/projects/${projectId}/swot/${swotId}/`
        : `http://localhost:8000/api/projects/${projectId}/swot/`;
      const method = swotId ? "PUT" : "POST";

      const response = await fetch(endpoint, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
        body: JSON.stringify(payload)
      });
      if (!response.ok) throw new Error("保存に失敗しました");
      const data = await response.json();
      if (onSave) onSave(data);
      console.log("保存成功:", data);
    } catch (err) {
      console.error("保存エラー:", err);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>SWOT 分析の共同編集</h2>
      {/* ここで全体の編集中ユーザー一覧を表示するなども可能 */}
      <div>
        <label>タイトル:</label>
        <input
          value={title}
          onChange={handleTitleChange}
          style={{ width: '100%', padding: '8px', marginBottom: '20px' }}
        />
      </div>
      {Object.keys(items).map((category) => (
        <div key={category} style={{ marginBottom: '20px' }}>
          <h3>{category}</h3>
          {items[category].map((item, index) => {
            // 各フィールドに対して、編集中状態なら色を変更してラベルを表示
            const fieldKey = `${category}-${index}`;
            const editingInfo = editingState[fieldKey];
            return (
              <div key={index} style={{ marginBottom: '10px', position: 'relative' }}>
                {editingInfo && (
                  <div style={{
                    position: 'absolute',
                    top: '-16px',
                    left: '0',
                    fontSize: '0.7em',
                    background: editingInfo.color,
                    padding: '2px 4px',
                    borderRadius: '4px',
                    color: '#fff'
                  }}>
                    {editingInfo.username}編集中
                  </div>
                )}
                <input
                  value={item}
                  onChange={(e) => handleItemChange(category, index, e.target.value)}
                  placeholder={`Enter ${category} idea`}
                  style={{
                    width: '100%',
                    padding: '8px',
                    border: editingInfo ? `2px solid ${editingInfo.color}` : '1px solid #ccc',
                    borderRadius: '4px'
                  }}
                  onFocus={() => startEditingField(category, index)}
                  onBlur={() => stopEditingField(category, index)}
                />
              </div>
            );
          })}
          <button type="button" onClick={() => handleAddItem(category)}>
            {category}項目を追加
          </button>
        </div>
      ))}
      <button onClick={handleSave}>保存</button>
    </div>
  );
}

export default CollaborativeSwotEditor;
