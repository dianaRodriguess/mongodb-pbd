from datetime import datetime
from bson import ObjectId


class Atividade:

    # status das atividades
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"

    STATUS_VALIDOS = [PENDENTE, EM_ANDAMENTO, CONCLUIDA]

    def __init__(
        self,
        titulo,
        descricao,
        responsavel_id,
        status=PENDENTE,
        prazo=None,
        _id=None,
        data_criacao=None,
        data_conclusao=None,
    ):

        self._id = _id
        self.titulo = titulo
        self.descricao = descricao
        self.responsavel_id = (
            ObjectId(responsavel_id)
            if isinstance(responsavel_id, str)
            else responsavel_id
        )
        self.status = status if status in self.STATUS_VALIDOS else self.PENDENTE
        self.prazo = prazo
        self.data_criacao = data_criacao or datetime.now()
        self.data_conclusao = data_conclusao

    def to_dict(self):
        atividade_dict = {
            "titulo": self.titulo,
            "descricao": self.descricao,
            "responsavel_id": self.responsavel_id,
            "status": self.status,
            "prazo": self.prazo,
            "data_criacao": self.data_criacao,
            "data_conclusao": self.data_conclusao,
        }

        if self._id:
            atividade_dict["_id"] = self._id

        return atividade_dict

    @staticmethod
    def from_dict(data):

        return Atividade(
            titulo=data.get("titulo"),
            descricao=data.get("descricao"),
            responsavel_id=data.get("responsavel_id"),
            status=data.get("status"),
            prazo=data.get("prazo"),
            _id=data.get("_id"),
            data_criacao=data.get("data_criacao"),
            data_conclusao=data.get("data_conclusao"),
        )

    def marcar_como_concluida(self):

        self.status = self.CONCLUIDA
        self.data_conclusao = datetime.now()

    def __str__(self):

        return (
            f"Atividade(id={self._id}, titulo={self.titulo}, "
            f"status={self.status}, responsavel={self.responsavel_id})"
        )

    def __repr__(self):
        return self.__str__()
