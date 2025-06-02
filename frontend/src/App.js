
import React, { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('http://localhost:5000/')
      .then(res => res.json())
      .then(data => setMessage(data.message));
  }, []);

  return (
    <div className="text-center p-6 text-xl font-bold">
      {message}
    </div>
  );
}

export default App;
