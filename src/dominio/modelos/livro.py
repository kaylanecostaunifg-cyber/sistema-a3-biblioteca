class Livro:
    """
    Classe de domínio para gestão do acervo de obras (RF04).
    """

    def __init__(self, id_livro: int, titulo: str, autor: str, isbn: str, ano: int, categoria: str):
        self._id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.ano = ano
        self.categoria = categoria

    @property
    def id_livro(self) -> int:
        return self._id_livro