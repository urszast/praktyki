from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from enum import Enum
import logging
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv



logging.basicConfig(level=logging.INFO)
app_description = "Aplikacja obsługuje zapytania pozwalające na: " \
                  "zaparzenie wybranej herbaty (czarna, zielona, owocowa, miętowa), " \
                  "monitorowanie dostępnych porcji herbat, " \
                  "możliwość dodania określonej ilości porcji"
app_namespace = "Tea_machine_fastApi"
app_title = "Tea_machine"

app = FastAPI(title=app_title, description=app_description)
# flask_app = Flask(__name__)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RodzajeHerbaty(str, Enum):
    czarna = "czarna"
    zielona = "zielona"
    owocowa = "owocowa"
    mietowa = "mietowa"


'''
il_czarna = 15
il_zielona = 3
il_owocowa = 7
il_mietowa = 2
'''

load_dotenv()


czarna = int(os.getenv("czarna") or 0)
zielona = int(os.getenv("zielona") or 0)
owocowa = int(os.getenv("owocowa") or 0)
mietowa = int(os.getenv("mietowa") or 0)


stan_poczatkowy = {"czarna": czarna, "zielona": zielona, "owocowa": owocowa, "mietowa": mietowa}
dostepne = stan_poczatkowy


class Herbata(BaseModel):
    rodzaj : str
    ilosc : int


class Czynnosc(BaseModel):
    wynik_czynnosci : str = Field(..., title="Wynik czynnosci")


@app.get('/tea/zaparzenie/{rodzaj}',
         summary="Zaparzenie herbaty",
         response_description="Wartości przesłanych danych",
         response_model=Czynnosc)
async def zaparzenie(rodzaj: RodzajeHerbaty = Path(...,
                                                   description="Przykładowy rodzaj herbaty",
                                                   examples='czarna')
                   ) -> Herbata:
    if dostepne[rodzaj] != 0:
        dostepne[rodzaj] -= 1
        komunikat = f"Zaparzono: herbata {rodzaj}. Zostało: {dostepne[rodzaj]}."
    else:
        komunikat = f"Brak herbaty {rodzaj} w automacie!"

    results = {"wynik_czynnosci": komunikat}
    return results


@app.get('/tea/sprawdzenie/{rodzaj}',
         summary="Sprawdzenie zawartości automatu",
         response_description="Wartości przesłanych danych",
         response_model=Czynnosc)
async def sprawdzenie(rodzaj: RodzajeHerbaty = Path(...,
                                                    description="Przykładowy rodzaj herbaty",
                                                    examples='czarna')
                   ) -> Herbata:
    komunikat = f"Dostępne: {dostepne[rodzaj]} x herbata {rodzaj}."
    results = {"wynik_czynnosci": komunikat}
    return results


@app.get('/tea/dodanie/{rodzaj}/{ilosc}',
         summary="Dodanie herbaty",
         response_description="Wartości przesłanych danych",
         response_model=Czynnosc)
async def dodanie(rodzaj: RodzajeHerbaty = Path(...,
                                                description="Przykładowy rodzaj herbaty",
                                                examples='czarna'),
                  ilosc: int = Path(...,
                                    description="Przykładowa ilosc dodanej herbaty",
                                    examples=1)
                   ) -> Herbata:
    dostepne[rodzaj] += ilosc
    komunikat = f"Dodano: {ilosc} x herbata {rodzaj}. Dostępne: {dostepne[rodzaj]}."
    results = {"wynik_czynnosci": komunikat}
    return results

