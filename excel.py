import pandas as pd
from datetime import datetime


def gerar_excel(produtos):
    data = []

    for p in produtos:
        data.append({
            "Nome": p["nome"],
            "Preço": f"R$ {p['preco']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "Link": p.get("link", "")
        })

    df = pd.DataFrame(data)

    filename = f"produtos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)

    return filename