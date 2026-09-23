from datetime import datetime
from infra.banco import obter_conexao
from dominio.modelos.emprestimo import Emprestimo
from dominio.modelos.aluno import Aluno
from dominio.modelos.professor import Professor
from dominio.modelos.livro import Livro

class RepositorioEmprestimoSQLite:
    def salvar(self, emprestimo: Emprestimo):
        """Salva um novo empréstimo no banco de dados."""
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO emprestimos (
                    id_usuario, id_livro, data_emprestimo, data_devolucao_prevista
                ) VALUES (?, ?, ?, ?)
            """, (
                emprestimo.usuario.id_usuario,
                emprestimo.livro.id_livro,
                emprestimo.data_emprestimo.strftime("%Y-%m-%d %H:%M:%S"),
                emprestimo.data_devolucao_prevista.strftime("%Y-%m-%d %H:%M:%S")
            ))
            conn.commit()

    def listar_todos(self) -> list:
        """Busca todos os empréstimos cadastrados."""
        emprestimos = []
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.id_emprestimo, e.data_emprestimo, e.data_devolucao_prevista, e.data_devolucao_real, e.valor_multa,
                       u.id_usuario, u.nome, u.email, u.tipo, u.matricula, u.departamento,
                       l.id_livro, l.titulo, l.autor, l.isbn, l.ano, l.categoria
                FROM emprestimos e
                JOIN usuarios u ON e.id_usuario = u.id_usuario
                JOIN livros l ON e.id_livro = l.id_livro
            """)
            linhas = cursor.fetchall()

            for linha in linhas:
                (id_emp, dt_emp, dt_prev, dt_real, multa,
                 id_u, nome_u, email_u, tipo_u, mat, dep,
                 id_l, tit_l, aut_l, isbn_l, ano_l, cat_l) = linha

                if tipo_u == "ALUNO":
                    usuario = Aluno(id_usuario=id_u, nome=nome_u, email=email_u, cpf="000.000.000-00", curso="Computação", matricula=mat)
                else:
                    usuario = Professor(id_usuario=id_u, nome=nome_u, email=email_u, departamento=dep)

                livro = Livro(id_livro=id_l, titulo=tit_l, autor=aut_l, isbn=isbn_l, ano=ano_l, categoria=cat_l)
                
                dt_emprestimo_obj = datetime.strptime(dt_emp, "%Y-%m-%d %H:%M:%S")
                emp = Emprestimo(usuario=usuario, livro=livro, data_emprestimo=dt_emprestimo_obj)
                emp.id_emprestimo = id_emp
                emp.valor_multa = multa
                
                if dt_real:
                    emp.data_devolucao_real = datetime.strptime(dt_real, "%Y-%m-%d %H:%M:%S")

                emprestimos.append(emp)
        return emprestimos

    def registrar_devolucao(self, id_emprestimo: int, data_devolucao_real: datetime, valor_multa: float):
        """Atualiza a data de devolução real e o valor da multa."""
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE emprestimos
                SET data_devolucao_real = ?, valor_multa = ?
                WHERE id_emprestimo = ?
            """, (
                data_devolucao_real.strftime("%Y-%m-%d %H:%M:%S"),
                valor_multa,
                id_emprestimo
            ))
            conn.commit()
    def listar_atrasados(self) -> list:
        """Retorna todos os empréstimos não devolvidos cuja data prevista já expirou."""
        agora_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        todos = self.listar_todos()
        
        # Filtra empréstimos sem devolução real e com data prevista menor que agora
        atrasados = [
            e for e in todos 
            if e.data_devolucao_real is None and e.data_devolucao_prevista < datetime.now()
        ]
        return atrasados