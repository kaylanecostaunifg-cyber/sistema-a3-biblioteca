from src.dominio.modelos.usuario import Usuario


class Aluno(Usuario):
    """
    Subclasse de Usuario que define regras específicas para Alunos.
    RF08 e RF09: Limite de 3 empréstimos e prazo de 7 dias.
    """

    def __init__(self, id_usuario: int, nome: str, email: str, cpf: str, matricula: str, curso: str):
        super().__init__(id_usuario, nome, email, cpf)
        self.matricula = matricula
        self.curso = curso

    def obter_limite_emprestimos(self) -> int:
        return 3

    def obter_prazo_devolucao_dias(self) -> int:
        return 7
