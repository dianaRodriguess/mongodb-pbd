from datetime import datetime
from bson import ObjectId


class Usuario:

    def __init__(self, nome, email, cargo=None, _id=None, data_criacao=None):

        self._id = _id
        self.nome = nome
        self.email = email
        self.cargo = cargo
        self.data_criacao = data_criacao or datetime.now()

    def to_dict(self):

        user_dict = {
            "nome": self.nome,
            "email": self.email,
            "cargo": self.cargo,
            "data_criacao": self.data_criacao,
        }

        if self._id:
            user_dict["_id"] = self._id

        return user_dict

    @staticmethod
    def from_dict(data):
        return Usuario(
            nome=data.get("nome"),
            email=data.get("email"),
            cargo=data.get("cargo"),
            _id=data.get("_id"),
            data_criacao=data.get("data_criacao"),
        )

    def __str__(self):
        return f"Usuario(id={self._id}, nome={self.nome}, email={self.email}, cargo={self.cargo})"

    def __repr__(self):
        return self.__str__()
