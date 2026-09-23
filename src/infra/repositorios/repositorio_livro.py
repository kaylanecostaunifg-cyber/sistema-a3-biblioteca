from infra.banco import obter_conexao
from dominio.modelos.aluno import Aluno
from dominio.modelos.professor import Professor
from dominio.modelos.livro import Livro  # <-- ADICIONE ESTA LINHA

class RepositorioLivroSQLite:
    def salvar(self, livro: Livro):
        """Salva ou atualiza um livro no banco de dados."""
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO livros (id_livro, titulo, autor, isbn, ano, categoria)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                livro.id_livro,
                livro.titulo,
                livro.autor,
                livro.isbn,
                getattr(livro, "ano", None),
                getattr(livro, "categoria", None)
            ))
            conn.commit()

    def listar_todos(self) -> list[Livro]:
        """Busca todos os livros salvos no SQLite."""
        livros = []
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_livro, titulo, autor, isbn, ano, categoria FROM livros")
            linhas = cursor.fetchall()

            for linha in linhas:
                id_l, titulo, autor, isbn, ano, categoria = linha
                livro = Livro(id_livro=id_l, titulo=titulo, autor=autor, isbn=isbn, ano=ano, categoria=categoria)
                livros.append(livro)
        return livros
    def buscar_por_titulo(self, termo: str) -> list[Livro]:
        """Busca livros que contenham o termo no título (busca parcial e sem case sensitive)."""
        livros = []
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_livro, titulo, autor, isbn, ano, categoria FROM livros WHERE titulo LIKE ?",
                (f"%{termo}%",)
            )
            linhas = cursor.fetchall()

            for linha in linhas:
                id_l, titulo, autor, isbn, ano, categoria = linha
                livro = Livro(
                    id_livro=id_l, 
                    titulo=titulo, 
                    autor=autor, 
                    isbn=isbn, 
                    ano=ano, 
                    categoria=categoria if categoria else "Geral"
                )
                livros.append(livro)
        return livros