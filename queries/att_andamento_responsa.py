from config.database import get_db

# CONSULTA 1: Atividades em Andamento com Responsável

def executar():
    print("\n" + "=" * 70)
    print("CONSULTA 1: Atividades em Andamento com Responsável")
    print("=" * 70)
    print("\nDescrição:")
    print("Lista atividades em andamento fazendo JOIN com usuários")
    print("para mostrar dados completos do responsável.\n")

    try:
        db = get_db()
        if db is not None:
            atividades = db["atividades"]
        else:
            print("Erro: get_db() retornou None")
            return []

        # pipeline
        pipeline = [
            {"$match": {"status": "em_andamento"}},
            {
                "$lookup": {
                    "from": "usuarios",
                    "localField": "responsavel_id",
                    "foreignField": "_id",
                    "as": "responsavel",
                }
            },
            {
                "$unwind": {
                    "path": "$responsavel",
                    "preserveNullAndEmptyArrays": True,
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "titulo": 1,
                    "descricao": 1,
                    "status": 1,
                    "prazo": 1,
                    "data_criacao": 1,
                    "responsavel.nome": 1,
                    "responsavel.email": 1,
                    "responsavel.cargo": 1,
                }
            },
            {"$sort": {"data_criacao": -1}},
        ]

        # executa o pipeline
        resultados = list(atividades.aggregate(pipeline))

        print(f"Encontradas {len(resultados)} atividades em andamento\n")

        if not resultados:
            print("Nenhuma atividade em andamento encontrada.\n")
        else:
            for i, atividade in enumerate(resultados, 1):
                print(f"{'─'*70}")
                print(f"Atividade {i}")
                print(f"{'─'*70}")
                print(f"ID: {atividade['_id']}")
                print(f"Título: {atividade['titulo']}")
                print(f"Descrição: {atividade['descricao']}")
                print(f"Status: {atividade['status']}")

                if "prazo" in atividade and atividade["prazo"]:
                    print(f"Prazo: {atividade['prazo'].strftime('%d/%m/%Y %H:%M')}")

                print(f"\nResponsável:")
                if "responsavel" in atividade:
                    resp = atividade["responsavel"]
                    print(f"   Nome: {resp.get('nome', 'N/A')}")
                    print(f"   Email: {resp.get('email', 'N/A')}")
                    print(f"   Cargo: {resp.get('cargo', 'N/A')}")
                else:
                    print("   Não atribuído")

                print()

        return resultados

    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return []


if __name__ == "__main__":
    from config.database import db_instance

    db_instance.connect()
    executar()
    db_instance.close()
