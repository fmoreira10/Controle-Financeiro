import React from 'react';

export default function Message({ text }) {
  return (
    <div className="text-center p-6 text-xl font-bold">
      {text || 'Nenhuma mensagem disponível.'}
    </div>
  );
}

