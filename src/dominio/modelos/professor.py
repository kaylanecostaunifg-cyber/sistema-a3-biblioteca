from src.dominio.modelos.usuario import Usuario


class Professor(Usuario):
    """
    Subclasse de Usuario que define regras específicas para Professores.
    RF08 e RF09: Limite de 5 empréstimos e prazo de 15 dias.
    """

    def __init__(self, id_usuario: int, nome: str, email: str, cpf: str, siape: str, departamento: str):
        super().__init__(id_usuario, nome, email, cpf)
        self.siape = siape
        self.departamento = departamento

    def obter_limite_emprestimos(self) -> int:
        return 5

    def obter_prazo_devolucao_dias(self) -> int:
        return 15