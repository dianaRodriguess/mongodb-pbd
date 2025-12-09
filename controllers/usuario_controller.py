from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from models.usuario import Usuario
from config.database import get_db

class UsuarioController:

    def __init__(self):
        self.db = get_db()
        if self.db is not None:
            self.collection = self.db["usuarios"]
            self.collection.create_index("email", unique=True)
        else:
            print("Error: get_db() returned None")

    def criar(self, nome, email, cargo=None):
        try:
            usuario = Usuario(nome=nome, email=email, cargo=cargo)
            resultado = self.collection.insert_one(usuario.to_dict())
            usuario._id = resultado.inserted_id

            print(f"Usuário criado: {usuario.nome} (ID: {usuario._id})")
            return usuario

        except DuplicateKeyError:
            print(f"Erro: Email '{email}' já está cadastrado!")
            return None
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return None

    def buscar_por_id(self, usuario_id):
        try:
            if isinstance(usuario_id, str):
                usuario_id = ObjectId(usuario_id)

            data = self.collection.find_one({"_id": usuario_id})

            if data:
                return Usuario.from_dict(data)
            else:
                print(f"Usuário não encontrado: {usuario_id}")
                return None

        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None

    def buscar_por_email(self, email):
        try:
            data = self.collection.find_one({"email": email})
            return Usuario.from_dict(data) if data else None
        except Exception as e:
            print(f"Erro ao buscar por email: {e}")
            return None

    def listar_todos(self):
        try:
            usuarios = []
            for data in self.collection.find():
                usuarios.append(Usuario.from_dict(data))

            print(f"Total de usuários: {len(usuarios)}")
            return usuarios

        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            return []

    def atualizar(self, usuario_id, nome=None, email=None, cargo=None):
        try:
            if isinstance(usuario_id, str):
                usuario_id = ObjectId(usuario_id)

            # Montar documento de atualização
            update_data = {}
            if nome:
                update_data["nome"] = nome
            if email:
                update_data["email"] = email
            if cargo:
                update_data["cargo"] = cargo

            if not update_data:
                print("Nenhum campo para atualizar!")
                return False

            resultado = self.collection.update_one(
                {"_id": usuario_id}, {"$set": update_data}
            )

            if resultado.modified_count > 0:
                print(f"Usuário atualizado: {usuario_id}")
                return True
            else:
                print(f"Nenhuma modificação realizada")
                return False

        except DuplicateKeyError:
            print(f"Erro: Email '{email}' já está em uso!")
            return False
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")
            return False

    def deletar(self, usuario_id):
        try:
            if isinstance(usuario_id, str):
                usuario_id = ObjectId(usuario_id)

            resultado = self.collection.delete_one({"_id": usuario_id})

            if resultado.deleted_count > 0:
                print(f"Usuário deletado: {usuario_id}")
                return True
            else:
                print(f"Usuário não encontrado: {usuario_id}")
                return False

        except Exception as e:
            print(f"Erro ao deletar usuário: {e}")
            return False

    def contar(self):
        return self.collection.count_documents({})
