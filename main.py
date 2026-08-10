from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

# 1. O MOLDE (A Planta da Tabela)
class Aluno(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str

# 2. A CHAVE DO COFRE (Conexão com o Docker do MT01)
DATABASE_URL = "postgresql://admin:senha_ultra_secreta@localhost:5432/smart_project"
engine = create_engine(DATABASE_URL)

# 3. O MOMENTO DE ABRIR O RESTAURANTE (Lifespan e Semente de Dados)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Magia 1: Cria a tabela Aluno sozinho!
    SQLModel.metadata.create_all(engine) 
    
    # Magia 2: Planta uma "Semente" (Seed) se o cofre estiver vazio.
    with Session(engine) as session:
        alunos_existentes = session.exec(select(Aluno)).all()
        if not alunos_existentes: # Se o banco tá vazio...
            aluno_cobaia = Aluno(nome="João Zezinho")
            session.add(aluno_cobaia)
            session.commit()
            
    yield # Restaurante Aberto!

# 4. INICIALIZAÇÃO DA API (O Balcão)
app = FastAPI(lifespan=lifespan)

# Libera o CORS (Para o Frontend poder pescar os dados depois)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. A NOSSA PRIMEIRA ROTA (O Prato do Menu)
@app.get("/alunos")
def ler_alunos():
    # Abre uma Sessão rápida no cofre e traz todos os alunos
    with Session(engine) as session:
        alunos = session.exec(select(Aluno)).all()
        return alunos