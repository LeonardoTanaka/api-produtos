from fastapi import FastAPI
from pydantic import BaseModel
from database import SessionLocal
from models import Produto
from excel import gerar_excel
from fastapi.responses import FileResponse
from email_service import enviar_email
from scraping import buscar_produtos
import pandas as pd


app = FastAPI()

# schema
class ProdutoSchema(BaseModel):
    nome: str
    preco: float


# home
@app.get("/")
def home():
    return {"status": "API online 🚀"}


# criar produto no banco
@app.post("/produto")
def criar_produto(produto: ProdutoSchema):
    db = SessionLocal()

    novo_produto = Produto(
        nome=produto.nome,
        preco=produto.preco
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return {"mensagem": "Produto salvo no banco!"}

# listar produtos do banco
@app.get("/produtos")
def listar_produtos():
    db = SessionLocal()
    produtos = db.query(Produto).all()

    return produtos

from excel import gerar_excel  # coloca lá em cima junto com os imports

@app.get("/exportar")
def exportar():
    db = SessionLocal()
    produtos = db.query(Produto).all()

    arquivo = gerar_excel(produtos)

    return FileResponse(
        path=arquivo,
        filename=arquivo,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

#@app.post("/exportar-email")
#def exportar_email(destinatario: str):
#    db = SessionLocal()
#    produtos = db.query(Produto).all()
#
#    arquivo = gerar_excel(produtos)

#    enviar_email(arquivo, destinatario)

#    return {"mensagem": "Email enviado com sucesso!"}


@app.get("/buscar")
def buscar(nome: str):
    produtos = buscar_produtos(nome)

    if not produtos:
        return {"erro": "Nenhum produto encontrado"}

    arquivo = gerar_excel(produtos)

    return FileResponse(
        path=arquivo,
        filename=arquivo,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )