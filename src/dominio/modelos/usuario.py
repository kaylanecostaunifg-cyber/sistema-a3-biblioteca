from abc import ABC, abstractmethod


class Usuario(ABC):
    """
    Classe abstrata base para representação de usuários no sistema.
    Aplica o conceito de encapsulamento e abstração de OO.
    """

    def __init__(self, id_usuario: int, nome: str, email: str, cpf: str):
        self._id_usuario = id_usuario
        self._nome = nome
        self._email = email
        self._cpf = cpf
        self._ativo = True

    @property
    def id_usuario(self) -> int:
        return self._id_usuario

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def email(self) -> str:
        return self._email

    @property
    def ativo(self) -> bool:
        return self._ativo

    @abstractmethod 
    def obter_limite_emprestimos(self) -> int:
        """Retorna o limite máximo de empréstimos simultâneos por perfil."""
        pass

    @abstractmethod
    def obter_prazo_devolucao_dias(self) -> int:
        """Retorna o prazo padrão de empréstimo em dias por perfil."""
        pass