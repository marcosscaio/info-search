from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db, SearchEntry
from scraper import search_info

app = FastAPI()

class SearchRequest(BaseModel):
    title: str

@app.post("/search/")
def search_moto(request: SearchRequest, db: Session = Depends(get_db)):
    price = search_info(request.title)
    if not price:
        raise HTTPException(status_code=404, detail="Moto não encontrada")
    
    entry = db.query(SearchEntry).filter(SearchEntry.title == request.title).first()

    if entry:
        entry.search_count += 1
        entry.price = price
    else:
        entry = SearchEntry(title=request.title, price=price, search_count=1)
        db.add(entry)
        
    db.commit()
    db.refresh(entry)
    
    return {"title": entry.title, "price": entry.price, "search_count": entry.search_count}

@app.get("/searches/")
def get_searches(db: Session = Depends(get_db)):
    return db.query(SearchEntry).all()

@app.delete("/search/{title}")
def delete_search(title: str, db: Session = Depends(get_db)):
    entry = db.query(SearchEntry).filter(SearchEntry.title == title).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Busca não encontrada")
    db.delete(entry)
    db.commit()
    return {"message": "Registro deletado com sucesso"}

