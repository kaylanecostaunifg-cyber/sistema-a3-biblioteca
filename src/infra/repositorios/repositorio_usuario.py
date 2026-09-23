from infra.banco import obter_conexao
from dominio.modelos.aluno import Aluno
from dominio.modelos.professor import Professor

class RepositorioUsuarioSQLite:
    def salvar(self, usuario):
        """Salva ou atualiza um Aluno ou Professor no banco de dados."""
        tipo = "ALUNO" if isinstance(usuario, Aluno) else "PROFESSOR"
        matricula = getattr(usuario, "matricula", None)
        departamento = getattr(usuario, "departamento", None)

        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO usuarios (id_usuario, nome, email, tipo, matricula, departamento)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (usuario.id_usuario, usuario.nome, usuario.email, tipo, matricula, departamento))
            conn.commit()

    def listar_todos(self):
        """Busca todos os usuários salvos no SQLite."""
        usuarios = []
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_usuario, nome, email, tipo, matricula, departamento FROM usuarios")
            linhas = cursor.fetchall()

            for linha in linhas:
                id_u, nome, email, tipo, matricula, departamento = linha
                if tipo == "ALUNO":
                    usuarios.append(Aluno(
                        id_usuario=id_u, 
                        nome=nome, 
                        email=email, 
                        cpf="000.000.000-00", 
                        curso="Ciência da Computação", 
                        matricula=matricula
                    ))
                else:
                    usuarios.append(Professor(
                        id_usuario=id_u, 
                        nome=nome, 
                        email=email, 
                        departamento=departamento
                    ))
        return usuarios