from fastapi import FastAPI
from app.database import Base, engine, SessionLocal
from app import models
import re

app = FastAPI()

Base.metadata.create_all(bind=engine)

def extract_amount(text):
    text = text.lower().replace(",", ".")
    
    # 🔹 caso 1: 15k / 15 k
    match = re.search(r"(\d+(\.\d+)?)\s*k", text)
    if match:
        return float(match.group(1)) * 1000

    # 🔹 caso 2: 15 lucas
    match = re.search(r"(\d+(\.\d+)?)\s*lucas?", text)
    if match:
        return float(match.group(1)) * 1000

    # 🔹 caso 3: números con punto (12.500)
    match = re.search(r"\d{1,3}(\.\d{3})+", text)
    if match:
        return float(match.group().replace(".", ""))

    # 🔹 caso 4: número simple
    match = re.search(r"\d+", text)
    if match:
        return float(match.group())

    return 0


def extract_category(text):
    text = text.lower()

    keywords = {
        "supermercado": ["super", "carrefour", "coto", "disco"],
        "servicios": ["luz", "gas", "agua", "internet"],
        "transporte": ["uber", "taxi", "sube", "colectivo"],
        "salida": ["bar", "cerveza", "resto", "restaurant"],
        "alquiler": ["alquiler", "renta"],
    }

    for category, words in keywords.items():
        for word in words:
            if word in text:
                return category

    return "otros"

@app.get("/")
def root():
    return {"message": "API funcionando"}


@app.post("/add")
def add_transaction(amount: float, category: str, description: str):
    db = SessionLocal()

    t = models.Transaction(
        amount=amount,
        category=category,
        description=description
    )

    db.add(t)
    db.commit()
    db.refresh(t)

    return {"message": "guardado", "id": t.id}

@app.post("/message")
def process_message(text: str):
    db = SessionLocal()

    amount = extract_amount(text)
    category = extract_category(text)

    if amount == 0:
        return {"error": "No pude detectar el monto"}

    t = models.Transaction(
        amount=amount,
        category=category,
        description=text,
        status="pending"
    )

    db.add(t)
    db.commit()
    db.refresh(t)

    return {
        "message": f"Registré ${amount} en {category}. ¿Confirmás?",
        "transaction_id": t.id
    }

@app.post("/confirm")
def confirm_transaction(transaction_id: int, confirm: bool):
    db = SessionLocal()

    t = db.query(models.Transaction).filter_by(id=transaction_id).first()

    if not t:
        return {"error": "No existe la transacción"}

    if confirm:
        t.status = "confirmed"
    else:
        t.status = "rejected"

    db.commit()

    return {"status": t.status}