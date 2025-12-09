from datetime import datetime
from bson import ObjectId
from models.atividade import Atividade
from config.database import get_db

class AtividadeController:

    def __init__(self):
        self.db = get_db()

        if self.db is not None:
            self.collection = self.db["atividades"]

            self.collection.create_index("responsavel_id")
            self.collection.create_index("status")
            self.collection.create_index("prazo")
        else:
            print("Error: get_db() returned None")

    def criar(self, titulo, descricao, responsavel_id, status="pendente", prazo=None):
        try:
            atividade = Atividade(
                titulo=titulo,
                descricao=descricao,
                responsavel_id=responsavel_id,
                status=status,
                prazo=prazo,
            )

            resultado = self.collection.insert_one(atividade.to_dict())
            atividade._id = resultado.inserted_id

            print(f"Atividade criada: {atividade.titulo} (ID: {atividade._id})")
            return atividade

        except Exception as e:
            print(f"Erro ao criar atividade: {e}")
            return None

    def buscar_por_id(self, atividade_id):
        try:
            if isinstance(atividade_id, str):
                atividade_id = ObjectId(atividade_id)

            data = self.collection.find_one({"_id": atividade_id})

            if data:
                return Atividade.from_dict(data)
            else:
                print(f"Atividade não encontrada: {atividade_id}")
                return None

        except Exception as e:
            print(f"Erro ao buscar atividade: {e}")
            return None

    def listar_todas(self):
        try:
            atividades = []
            for data in self.collection.find():
                atividades.append(Atividade.from_dict(data))

            print(f"Total de atividades: {len(atividades)}")
            return atividades

        except Exception as e:
            print(f"Erro ao listar atividades: {e}")
            return []

    def listar_por_status(self, status):
        try:
            atividades = []
            for data in self.collection.find({"status": status}):
                atividades.append(Atividade.from_dict(data))

            print(f"Atividades com status '{status}': {len(atividades)}")
            return atividades

        except Exception as e:
            print(f"Erro ao buscar por status: {e}")
            return []

    def listar_por_responsavel(self, responsavel_id):
        try:
            if isinstance(responsavel_id, str):
                responsavel_id = ObjectId(responsavel_id)

            atividades = []
            for data in self.collection.find({"responsavel_id": responsavel_id}):
                atividades.append(Atividade.from_dict(data))

            print(f"Atividades do responsável: {len(atividades)}")
            return atividades

        except Exception as e:
            print(f"Erro ao buscar por responsável: {e}")
            return []

    def atualizar(
        self,
        atividade_id,
        titulo=None,
        descricao=None,
        status=None,
        prazo=None,
        responsavel_id=None,
    ):
        try:
            if isinstance(atividade_id, str):
                atividade_id = ObjectId(atividade_id)

            update_data = {}
            if titulo:
                update_data["titulo"] = titulo
            if descricao:
                update_data["descricao"] = descricao
            if status:
                if status in Atividade.STATUS_VALIDOS:
                    update_data["status"] = status

                    if status == Atividade.CONCLUIDA:
                        update_data["data_conclusao"] = datetime.now()
                else:
                    print(f"Status inválido: {status}")
                    return False
            if prazo:
                update_data["prazo"] = prazo
            if responsavel_id:
                if isinstance(responsavel_id, str):
                    responsavel_id = ObjectId(responsavel_id)
                update_data["responsavel_id"] = responsavel_id

            if not update_data:
                print("Nenhum campo para atualizar!")
                return False

            resultado = self.collection.update_one(
                {"_id": atividade_id}, {"$set": update_data}
            )

            if resultado.modified_count > 0:
                print(f"Atividade atualizada: {atividade_id}")
                return True
            else:
                print(f"Nenhuma modificação realizada")
                return False

        except Exception as e:
            print(f"Erro ao atualizar atividade: {e}")
            return False

    def deletar(self, atividade_id):
        try:
            if isinstance(atividade_id, str):
                atividade_id = ObjectId(atividade_id)

            resultado = self.collection.delete_one({"_id": atividade_id})

            if resultado.deleted_count > 0:
                print(f"Atividade deletada: {atividade_id}")
                return True
            else:
                print(f"Atividade não encontrada: {atividade_id}")
                return False

        except Exception as e:
            print(f"Erro ao deletar atividade: {e}")
            return False

    def contar(self):
        return self.collection.count_documents({})

    def contar_por_status(self, status):
        return self.collection.count_documents({"status": status})
