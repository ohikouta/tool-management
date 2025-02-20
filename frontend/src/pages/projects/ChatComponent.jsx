import React, { useEffect, useState } from 'react';

function ChatComponent({ roomId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [socket, setSocket] = useState(null);

  

  useEffect(() => {
    // WebSocket 接続
    const newSocket = new WebSocket(`ws://localhost:8000/ws/chat/${roomId}/`);
    setSocket(newSocket);
    console.log('WebSocket connected');
    // メッセージ受信時の処理
    newSocket.onmessage = (e) => {
      const data = JSON.parse(e.data);
      setMessages(prev => [...prev, data.message]);
    };

    // クリーンアップ
    return () => {
      newSocket.close();
    };
  }, [roomId]);

  const sendMessage = () => {
    if (socket && input.trim()) {
      socket.send(JSON.stringify({ message: input }));
      setInput('');
    }
  };

  return (
    <div>
      <div style={{ border: '1px solid #ccc', height: '200px', overflowY: 'auto' }}>
        {messages.map((msg, index) => (
          <div key={index}>{msg}</div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
      />
      <button onClick={sendMessage}>送信</button>
    </div>
  );
}

export default ChatComponent;
