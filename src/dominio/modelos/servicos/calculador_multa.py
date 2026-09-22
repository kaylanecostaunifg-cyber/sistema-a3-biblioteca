from datetime import datetime
from src.dominio.modelos.emprestimo import Emprestimo


class CalculadorMulta:
    def __init__(self, valor_diaria: float = 2.0):
        """
        Calculador de multa por atraso.
        :param valor_diaria: Valor da multa por dia de atraso (Padrão: R$ 2,00/dia).
        """
        self.valor_diaria = valor_diaria

    def calcular_multa(self, emprestimo: Emprestimo) -> float:
        """
        Calcula o valor total da multa para um determinado empréstimo.
        Se não houver atraso, o valor retornado é 0.0.
        """
        data_devolucao = emprestimo.data_devolucao_real or datetime.now()

        if data_devolucao <= emprestimo.data_devolucao_prevista:
            return 0.0

        dias_atraso = (data_devolucao - emprestimo.data_devolucao_prevista).days

        if dias_atraso == 0 and data_devolucao > emprestimo.data_devolucao_prevista:
            dias_atraso = 1

        return dias_atraso * self.valor_diaria