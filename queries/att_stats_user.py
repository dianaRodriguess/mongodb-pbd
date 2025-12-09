from config.database import get_db

# CONSULTA COMPLEXA 2: Estatísticas de Atividades por Usuário

def executar():
    print("\n" + "=" * 70)
    print("CONSULTA 2: Estatísticas de Atividades por Usuário")
    print("=" * 70)
    print("\nDescrição:")
    print("Agrupa atividades por usuário e calcula estatísticas")
    print("detalhadas incluindo taxa de conclusão.\n")

    try:
        db = get_db()
        if db is not None:
            atividades = db["atividades"]
        else:
            print("Erro: get_db() retornou None")
            return []

        # pipeline
        pipeline = [
            {
                "$lookup": {
                    "from": "usuarios",
                    "localField": "responsavel_id",
                    "foreignField": "_id",
                    "as": "responsavel",
                }
            },
            {"$unwind": {"path": "$responsavel", "preserveNullAndEmptyArrays": True}},
            {
                "$group": {
                    "_id": {
                        "usuario_id": "$responsavel_id",
                        "usuario_nome": "$responsavel.nome",
                        "usuario_email": "$responsavel.email",
                        "usuario_cargo": "$responsavel.cargo",
                    },
                    "total_atividades": {"$sum": 1},
                    "pendentes": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$status", "pendente"]},
                                1,
                                0,
                            ]
                        }
                    },
                    "em_andamento": {
                        "$sum": {"$cond": [{"$eq": ["$status", "em_andamento"]}, 1, 0]}
                    },
                    "concluidas": {
                        "$sum": {"$cond": [{"$eq": ["$status", "concluida"]}, 1, 0]}
                    },
                    "atividades": {
                        "$push": {
                            "titulo": "$titulo",
                            "status": "$status",
                            "prazo": "$prazo",
                        }
                    },
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "usuario_id": "$_id.usuario_id",
                    "nome": "$_id.usuario_nome",
                    "email": "$_id.usuario_email",
                    "cargo": "$_id.usuario_cargo",
                    "total_atividades": 1,
                    "pendentes": 1,
                    "em_andamento": 1,
                    "concluidas": 1,
                    "atividades": 1,
                    "percentual_conclusao": {
                        "$cond": [
                            {"$eq": ["$total_atividades", 0]},
                            0,
                            {
                                "$multiply": [
                                    {"$divide": ["$concluidas", "$total_atividades"]},
                                    100,
                                ]
                            },
                        ]
                    },
                }
            },
            {"$sort": {"total_atividades": -1}},
        ]

        # executa o pipeline
        resultados = list(atividades.aggregate(pipeline))

        print(f"Estatísticas de {len(resultados)} usuários\n")

        if not resultados:
            print("Nenhum usuário com atividades encontrado.\n")
        else:
            for i, usuario in enumerate(resultados, 1):
                print(f"{'═'*70}")
                print(f"Usuário {i}")
                print(f"{'═'*70}")
                print(f"Nome: {usuario.get('nome', 'N/A')}")
                print(f"Email: {usuario.get('email', 'N/A')}")
                print(f"Cargo: {usuario.get('cargo', 'N/A')}")

                print(f"\nEstatísticas de Atividades:")
                print(f"{'─'*70}")
                print(f"   Total de atividades: {usuario['total_atividades']}")
                print(
                    f"   • Pendentes: {usuario['pendentes']} "
                    f"({usuario['pendentes']/usuario['total_atividades']*100:.1f}%)"
                )
                print(
                    f"   • Em andamento: {usuario['em_andamento']} "
                    f"({usuario['em_andamento']/usuario['total_atividades']*100:.1f}%)"
                )
                print(
                    f"   • Concluídas: {usuario['concluidas']} "
                    f"({usuario['concluidas']/usuario['total_atividades']*100:.1f}%)"
                )
                print(f"\nTaxa de conclusão: {usuario['percentual_conclusao']:.1f}%")

                if usuario.get("atividades"):
                    print(f"\nLista de Atividades:")
                    print(f"{'─'*70}")
                    for j, ativ in enumerate(usuario["atividades"], 1):
                        status_emoji = {
                            "pendente": "⏳",
                            "em_andamento": "🔄",
                            "concluida": "✅",
                        }
                        emoji = status_emoji.get(ativ["status"], "📌")

                        prazo_str = ""
                        if ativ.get("prazo"):
                            prazo_str = (
                                f" [Prazo: {ativ['prazo'].strftime('%d/%m/%Y')}]"
                            )

                        print(
                            f"   {j}. {emoji} {ativ['titulo']} ({ativ['status']}){prazo_str}"
                        )

                print()

        return resultados

    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return []


if __name__ == "__main__":
    # Permite executar a consulta diretamente
    from config.database import db_instance

    db_instance.connect()
    executar()
    db_instance.close()
