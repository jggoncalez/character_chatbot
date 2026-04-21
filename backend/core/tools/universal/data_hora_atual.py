from datetime import datetime

_DIAS_SEMANA = {
    0: "segunda-feira",
    1: "terça-feira",
    2: "quarta-feira",
    3: "quinta-feira",
    4: "sexta-feira",
    5: "sábado",
    6: "domingo",
}


def data_hora_atual() -> dict:
    now = datetime.now()
    dia = _DIAS_SEMANA[now.weekday()]
    return {
        "data": now.strftime("%d/%m/%Y"),
        "hora": now.strftime("%H:%M"),
        "dia_semana": dia,
        "data_completa": f"{dia}, {now.strftime('%d de %B de %Y')}",
    }


if __name__ == "__main__":
    print(data_hora_atual())
