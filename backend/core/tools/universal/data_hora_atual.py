def data_hora_atual() -> dict:
    from datetime import datetime
    now = datetime.now()

    dias = {
        0: "segunda-feira",
        1: "terça-feira",
        2: "quarta-feira",
        3: "quinta-feira",
        4: "sexta-feira",
        5: "sábado",
        6: "domingo",
    }

    return {
        "data": now.strftime("%d/%m/%Y"),
        "hora": now.strftime("%H:%M"),
        "dia_semana": dias[now.weekday()],
        "data_completa": f"{dias[now.weekday()]}, {now.strftime('%d de %B de %Y')}",
    }

if __name__ == "__main__":
    print(data_hora_atual())