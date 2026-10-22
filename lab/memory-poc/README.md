# AI FOR AI LAB — Memory POC

Wynik i ograniczenia: **REPORT.md**. Snapshot: 2026-10-22. Lokalny POC; brak zmian w agentach, harmonogramach lub repozytoriach zdalnych.

Wymagania: Python 3.10+, wyłącznie biblioteka standardowa. Nie potrzeba kluczy API, dostępu do sieci ani instalacji pakietów.

Uruchom z katalogu paczki:

```bash
python evaluate.py
python -m unittest discover -s . -p 'test_*.py' -v
python demo.py
```

`evaluate.py` sprawdza hashe źródeł i zamrożonych danych. Nie usuwać `protocol_lock.json` po zmianie danych: nowy eksperyment powinien mieć oddzielny katalog i protokół.

Przykład użycia pamięci:

```python
import json
from pathlib import Path
from memory import Memory
engine = Memory(json.loads(Path('memories.json').read_text()))
context = engine.retrieve('distutils regression control cache_tag install_lib', 114)
for item in context:
    print(item['id'], item['source_session'], item['lesson'])
engine.save('state.json')
engine = Memory.load('state.json')
```

Zawartość:

- `memory.py`: wyszukiwanie BM25, filtr czasu i widoczności, wygaszanie zastąpionych lekcji, Q/EMA, deduplikacja feedbacku, zapis/odczyt stanu, eksperymentalna reguła nagrody i wybór zadania.
- `memories.json`: 22 ręcznie opracowane lekcje; `build_dataset.py` dokumentuje ich pochodzenie i sposób utworzenia.
- `episodes.json`: 152 sekcje historii; `source/`: oryginalny snapshot dziennika i ledger.
- `cases.json`: 20 ręcznych zapytań z oczekiwaną przydatną wcześniejszą lekcją.
- `evaluate.py`: chronologiczny replay wyszukiwania, bez wywołań modeli. Gold jest używany po retrieval, jako PROXY feedbacku, nigdy jako jego wejście.
- `test_memory.py`: testy mechanizmów i kontrprzykładów; `demo.py`: jawnie syntetyczne przykłady nagród i selekcji.
- `results/`: wyniki, pełne ślady wyboru, testy, stan demonstracyjny, analiza wag, wcześniejszy przebieg i protokoły.

Kod jest niezależną adaptacją pomysłów z publikacji. Nie skopiowano implementacji autorów. Nie jest to pełna reprodukcja ExpeL, Reflexion ani MemRL. Automatyczna ekstrakcja/refleksja przez LLM, embeddingi, uwierzytelnianie API i produkcyjna orkiestracja są poza zakresem.

Filtr `owner`/`visibility` to logika POC, NIE izolacja bezpieczeństwa. Nie umieszczać prawdziwej prywatnej pamięci dwóch agentów w tym samym dostępnym im pliku. `verified=True` jest wejściem zaufanego testu, NIE potwierdzeniem tożsamości ewaluatora. Wdrożenie wymaga niezależnego źródła feedbacku i kontroli dostępu.
