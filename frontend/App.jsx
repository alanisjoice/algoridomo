import { useState, useEffect } from 'react'
import './App.css'

function App() {
  // 1. A Memória da Tela (Onde os dados vão ficar)
  const [alunos, setAlunos] = useState([])

  // 2. O Gatilho de Disparo (Faça isso quando a tela abrir)
  useEffect(() => {
    fetch('http://localhost:8000/alunos')
      .then(resposta => resposta.json())
      .then(dados => setAlunos(dados))
  }, [])

  // 3. O Desenho da Vitrine
  return (
    <div className="painel">
      <h1>🚀 SaaS Smart Project</h1>
      <div className="lista-cards">
        {alunos.map(aluno => (
          <div key={aluno.id} className="card-aluno">
            <h2>{aluno.nome}</h2>
          </div>
        ))}
      </div>
    </div>
  )
}