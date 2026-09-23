import sys
from pathlib import Path

# Garante que o Python encontre a pasta src
RAIZ = Path(__file__).resolve().parent
sys.path.append(str(RAIZ / "src"))

from infra.banco import inicializar_banco
from infra.repositorios.repositorio_usuario import RepositorioUsuarioSQLite
from infra.repositorios.repositorio_livro import RepositorioLivroSQLite
from dominio.modelos.aluno import Aluno
from dominio.modelos.livro import Livro

def testar_persistencia():
    # 1. Garante que o banco e as tabelas existem
    inicializar_banco()

    # 2. Instancia os repositórios
    repo_usuario = RepositorioUsuarioSQLite()
    repo_livro = RepositorioLivroSQLite()

    # 3. Cria dados de teste
    # 3. Cria dados de teste (adicionados cpf e curso)
    aluno_teste = Aluno(
        id_usuario=1, 
        nome="Kaylane Costa", 
        email="kaylane@email.com", 
        cpf="123.456.789-00", 
        curso="Ciência da Computação", 
        matricula="1352522416"
    )
    # 3. Cria dados de teste (adicionada a categoria)
    livro_teste = Livro(
        id_livro=101, 
        titulo="Engenharia de Software", 
        autor="Ian Sommerville", 
        isbn="9788579361081", 
        ano=2019, 
        categoria="Tecnologia"
    )

    # 4. Salva no Banco SQLite
    print("\n Salvando registros no SQLite...")
    repo_usuario.salvar(aluno_teste)
    repo_livro.salvar(livro_teste)
    print("Registros salvos com sucesso!")

    # 5. Le de volta do Banco para comprovar que funcionou
    print("\n🔍 Lendo registros salvos do banco de dados:")
    
    usuarios_salvos = repo_usuario.listar_todos()
    for u in usuarios_salvos:
        print(f" Usuário no BD: ID {u.id_usuario} | {u.nome} ({u.email}) - Matrícula: {u.matricula}")

    livros_salvos = repo_livro.listar_todos()
    for l in livros_salvos:
        print(f" Livro no BD: ID {l.id_livro} | {l.titulo} por {l.autor} (ISBN: {l.isbn})")

if __name__ == "__main__":
    testar_persistencia()