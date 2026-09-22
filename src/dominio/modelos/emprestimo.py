from datetime import datetime, timedelta
from typing import Optional
from src.dominio.modelos.usuario import Usuario
from src.dominio.modelos.livro import Livro


class Emprestimo:
    def __init__(self, id_emprestimo: int, usuario: Usuario, livro: Livro, data_emprestimo: Optional[datetime] = None):
        self._id_emprestimo = id_emprestimo
        self._usuario = usuario
        self._livro = livro
        self._data_emprestimo = data_emprestimo or datetime.now()
        
        # O prazo é calculado dinamicamente conforme o perfil (Aluno = 7 dias, Professor = 15 dias)
        dias_prazo = self._usuario.obter_prazo_devolucao_dias()
        self._data_devolucao_prevista = self._data_emprestimo + timedelta(dias=dias_prazo)
        
        self._data_devolucao_real: Optional[datetime] = None
        self._status = "ATIVO"  # ATIVO, CONCLUIDO, ATRASADO

    @property
    def id_emprestimo(self) -> int:
        return self._id_emprestimo

    @property
    def usuario(self) -> Usuario:
        return self._usuario

    @property
    def livro(self) -> Livro:
        return self._livro

    @property
    def data_emprestimo(self) -> datetime:
        return self._data_emprestimo

    @property
    def data_devolucao_prevista(self) -> datetime:
        return self._data_devolucao_prevista

    @property
    def data_devolucao_real(self) -> Optional[datetime]:
        return self._data_devolucao_real

    @property
    def status(self) -> str:
        if self._data_devolucao_real is None and datetime.now() > self._data_devolucao_prevista:
            return "ATRASADO"
        return self._status

    def realizar_devolucao(self, data_devolucao: Optional[datetime] = None) -> None:
        """Registra a devolução do livro e atualiza o status."""
        self._data_devolucao_real = data_devolucao or datetime.now()
        self._status = "CONCLUIDO"

    def esta_atrasado(self) -> bool:
        """Verifica se o empréstimo está com devolução em atraso."""
        data_referencia = self._data_devolucao_real or datetime.now()
        return data_referencia > self._data_devolucao_prevista