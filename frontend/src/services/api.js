// src/services/api.js
const API_URL = 'http://localhost:5000';

export async function fetchMessage() {
  const response = await fetch(`${API_URL}/`);
  if (!response.ok) throw new Error('Erro ao buscar mensagem');
  return response.json();
}
