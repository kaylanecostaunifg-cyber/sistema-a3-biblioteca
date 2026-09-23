import sqlite3
from pathlib import Path

def obter_conexao():
    """Retorna a conexão com o arquivo do banco SQLite."""
    raiz = Path(__file__).resolve().parent.parent.parent
    caminho_db = raiz / "dados" / "biblioteca.db"
    caminho_db.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(caminho_db)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def inicializar_banco():
    """Cria as tabelas no arquivo do banco se elas não existirem."""
    with obter_conexao() as conn:
        cursor = conn.cursor()
        
        # Tabela de Usuários (Alunos e Professores)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                tipo TEXT NOT NULL CHECK(tipo IN ('ALUNO', 'PROFESSOR')),
                matricula TEXT,
                departamento TEXT
            )
        """)
        
        # Tabela de Livros
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id_livro INTEGER PRIMARY KEY,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                isbn TEXT NOT NULL,
                ano INTEGER,
                categoria TEXT
            )
        """)
        
        # Tabela de Empréstimos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emprestimos (
                id_emprestimo INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                id_livro INTEGER NOT NULL,
                data_emprestimo TEXT NOT NULL,
                data_devolucao_prevista TEXT NOT NULL,
                data_devolucao_real TEXT,
                valor_multa REAL DEFAULT 0.0,
                FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario),
                FOREIGN KEY (id_livro) REFERENCES livros (id_livro)
            )
        """)
        
        conn.commit()
        print("Banco de dados criado e inicializado com sucesso!")

if __name__ == "__main__":
    inicializar_banco()