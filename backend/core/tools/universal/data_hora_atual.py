def data_hora_atual() -> dict:
    from datetime import datetime
    now = datetime.now()
    return {
        "data": now.strftime("%d/%m/%Y"),
        "hora": now.strftime("%H:%M"),
        "dia_semana": now.strftime("%A")
    }
    
if __name__ == "__main__":
    print(data_hora_atual())