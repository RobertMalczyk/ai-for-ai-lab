import json,collections
from pathlib import Path
p=Path(__file__).parent
results=json.loads((p/'results/retrieval.json').read_text());manifest=json.loads((p/'source_manifest.json').read_text())
ledger=[json.loads(x) for x in (p/'source/sessions.jsonl').read_text().splitlines() if x.strip()]
counts=dict(collections.Counter(x['outcome'] for x in ledger))
rows='\n'.join(f"| {name} | {r['hits']}/{r['n']} | {r['mean_recall_at_3']:.1%} | {r['mean_context_chars']:.0f} |" for name,r in results.items())
details='\n'.join(f"| {t['case']} | {', '.join(t['expected'])} | {', '.join(t['retrieved'])} | {'TAK' if t['hit'] else 'NIE'} |" for t in results['lexical']['traces'])
text=f'''# POC pamięci agentów — wynik i decyzja

Data: 22 października 2026. **GREEN LIGHT dla ograniczonego pilotażu pamięci lekcji. Brak green light dla autonomicznego sterowania nagrodami.**

## Wybór publikacji

1. **ExpeL**, [AAAI / arXiv:2308.10144](https://arxiv.org/abs/2308.10144): główna inspiracja dla warunkowych lekcji wyprowadzanych z sukcesów i porażek. W POC lekcje opracował ręcznie autor; nie uruchomiono automatycznej ekstrakcji ExpeL.
2. **Reflexion**, [arXiv:2303.11366](https://arxiv.org/abs/2303.11366): zapamiętanie błędu i korekty przed kolejną próbą. POC odtwarza przechowywanie i przywołanie już zapisanych refleksji; nie wykonuje nowych prób LLM.
3. **MemRL**, [arXiv:2601.03192v1](https://arxiv.org/html/2601.03192v1): wariant eksperymentalny z dwustopniowym retrieval i aktualizacją użyteczności pamięci. W POC BM25 zastępuje embeddingi, a ocena przydatności pochodzi z ręcznych etykiet trafności, nie z nowych wyników zadań. To adaptacja, nie reprodukcja pracy.

Voyager i motywacja przez learning progress pozostają poza rdzeniem tego etapu: w historii nie ma dostatecznie porównywalnych prób do wiarygodnego oszacowania przyrostu kompetencji. Dodano jedynie jawnie syntetyczną demonstrację wyboru zadania z ograniczoną premią za możliwość uczenia.

## Dane i pochodzenie

Źródło: [RobertMalczyk/ai-for-ai-lab](https://github.com/RobertMalczyk/ai-for-ai-lab), commit `{manifest['commit']}`.
[SESSIONS.md w snapshotcie](https://github.com/RobertMalczyk/ai-for-ai-lab/blob/{manifest['commit']}/docs/SESSIONS.md).

- 152 sekcje sesji i 152 wiersze ledger.
- Oryginalne etykiety wyników: `{counts}`.
- 22 ręcznie opracowane lekcje oraz 20 wybranych zapytań historycznych.
- Źródła i ich SHA-256 znajdują się w `source_manifest.json`.
- Lekcja jest dostępna dopiero PO sesji źródłowej. Korekta zapisana na końcu sesji działa od następnej sesji.
- Korzystamy z aktualnego, przypiętego snapshotu. Dziennik zawiera również późniejsze korekty. Nie odtworzono wszystkich historycznych wersji Git; chronologia numerów nie gwarantuje pełnego braku retrospektywnej informacji.

## Co wykonano

Implementacja Python, bez zależności, kluczy i sieci: pamięć trwała, BM25, wybór maksymalnie trzech lekcji, filtrowanie sesji/ważności/widoczności, zastępowanie błędnych reguł, EMA wartości Q, deduplikacja zdarzenia feedbacku także po restarcie. Waga Q wynosi 0.25; α=0.2; Q początkowe=0.5. Znormalizowana trafność leksykalna ogranicza zbiór do maksymalnie ośmiu kandydatów przed rerankingiem. Q nie może wprowadzić pamięci o zerowym dopasowaniu.

Użyteczność aktualizujemy według `Q_new = Q_old + alpha * ((reward+1)/2 - Q_old)`. W ocenie historycznej reward wynosi +1 dla karty wskazanej przez ręczną etykietę i -1 dla pozostałych przywołanych kart. To **uczenie rankingu według proxy trafności**, a nie dowód, że dana karta spowodowała sukces. Nie wykorzystujemy etykiet `negative` z ledger jako kar.

Zamrożono dane i parametry przed pierwszym wykonaniem. Zachowano pierwszy wynik oraz zapis poprawki: v1 zbyt wcześnie wyłączała kartę zastąpioną na końcu bieżącej sesji. Poprawiono granicę czasową i usunięto z karty 047 sformułowanie pełniejszej procedury z sesji 049. Następnie dodano trwały zapis stanu, bez strojenia rankingu. Pierwotne wyniki są w `results/v1/`; lock kolejnej wersji również zachowano. Nie jest to zewnętrzna prerejestracja.

## Wynik wyszukiwania

Sukces oznacza: w trzech zwróconych pozycjach znajduje się co najmniej jedna **ręcznie wskazana użyteczna wcześniejsza lekcja**. Nie oznacza poprawnej decyzji modelu ani wykonania zadania.

| Wariant | Trafienia hit@3 | Średni recall@3 | Średnia liczba znaków treści |
|---|---:|---:|---:|
{rows}

`recent`: trzy ostatnie dostępne karty. `raw_bm25`: trzy sekcje oryginalnego dziennika. `lexical`: trzy dopasowane karty lekcji. `utility`: te same karty z uczonym proxy użyteczności. Dla tekstu surowego dopasowanie jest zaliczane tylko wtedy, gdy sekcja jest źródłem oczekiwanej karty.

**Nie traktować 14→19 jako wzrostu skuteczności agentów.** Baseline surowego tekstu może zwrócić inną, również użyteczną sekcję, której ręczna lista gold nie uwzględnia. Karty i zapytania opracował ten sam autor po poznaniu wyników. Karty mają inny poziom kondensacji niż sekcje, a konteksty nie są wyrównane pod względem długości. Liczba znaków obejmuje tylko treść, bez metadanych i promptów; nie jest liczbą tokenów, kosztem API ani pomiarem pełnego narzutu. Nie porównano z faktycznym obecnym agentem czytającym AGENTS/STATE i historię.

Wagi Q 0, 0.1, 0.25 i 0.5 dały po 19/20 hit@3. Brak dowodu dodatkowej korzyści z komponentu MemRL. Nie wybierano najlepszej wagi na podstawie wyników.

## Co nie zadziałało

C118: pytanie o dowody do publikowanej narracji nie przywołało wskazanej pamięci o brakujących surowych artefaktach / datowanych twierdzeniach. BM25 dopasował inne lekcje o dowodach. To rzeczywista granica POC: przeniesienie lekcji między tematami o innym słownictwie. Nie dostrajano słownika po tej porażce. W pilotażu należy porównać embeddingi lub doprecyzowanie zapytania na nowych przypadkach.

## Zmiana błędnej lekcji na przykładzie LAB-u

Sesja 046: ograniczenie odczytu do ostatniej sekcji miało lokalny sukces w liczbie bajtów. Sesja 047: Agent 2 wykazał utratę własnego kontekstu Agent 1. Sesja 049: poprawiona procedura zachowała trzy potrzebne sekcje. POC wycofuje kartę 046 po korekcie 047 i zastępuje roboczą kartę 047 po sesji 049. Nawet Q=1 nie przywraca unieważnionej karty. Wycofanie jest ręcznie oznaczone z historii; automatyczne wykrywanie sprzeczności przez model nie zostało sprawdzone.

## Nagrody i motor działania

`results/demo.json` zawiera syntetyczne przeliczenia inspirowane historią, nie zaobserwowane reakcje agentów:

- trafny pre-flight Click: +0.2 za nowe sprawdzone ustalenie;
- review distutils wykrywające błędną kontrolę: +0.5;
- czekanie na maintainerów: brak aktualizacji, nie kara;
- powtórne sprawdzenie bez nowego wyniku: 0;
- powtórzenie znanego błędu: -0.5.

Nie karać za obalenie hipotezy ani za ujawnienie błędu. Wspomnienie o porażce może zwiększyć Q po późniejszym użytecznym zastosowaniu; demo zachowuje wzrost 0.5→0.6 także po zapisie i odczycie stanu.

Selekcja zadań najpierw odrzuca niedopuszczalne, nieaktywne i pozbawione zewnętrznej wartości. Dopiero potem używa ograniczonej premii za możliwość uczenia i kosztu. Demo wybiera dopuszczalnego zewnętrznego kandydata zamiast sprawdzania niezmienionego PR-a lub budowy narzędzia tylko dla LAB-u. Wartości wejściowe są podane ręcznie; to test logiki, nie dowód autonomicznej inicjatywy ani pomiar learning progress.

Ryzyko pozostające: premia za nowe odrzucenia może zachęcać do łatwego masowego odrzucania kandydatów. W pilotażu liczyć ją obserwacyjnie, z limitem budżetu discovery i deduplikacją według dowodu/issue, a nie swobodnie nadawanego ID. Nie aktywować selekcji według tej nagrody przed porównaniem prospektywnym.

## Weryfikacja

**20/20 testów technicznych**: filtr czasu, moment korekty, brak przywoływania wycofanego sukcesu, separacja logiczna prywatnych kart, blokada modyfikacji cudzej karty, trwałość pamięci i deduplikacji po restarcie, brak kary za oczekiwanie/blokadę, brak punktów za samą czynność, możliwość wartościowej lekcji z porażki, odrzucenie niepotwierdzonego feedbacku i niepowiązanej karty o wysokim Q, ograniczenia selekcji zadania. Pełny log: `results/tests.txt`.

Testy sprawdzają implementację wymyślonych zasad, nie ich skuteczność u modeli. Flagę `verified` przekazuje zaufany test; brak produkcyjnego uwierzytelniania. Filtr prywatności nie zastępuje osobnych repozytoriów/uprawnień. Nie przeprowadzono ślepego A/B z dwoma agentami, treningu modeli ani nowych działań OSS.

## Decyzja wdrożeniowa

**Tak dla V1: pamięć lekcji + refleksje + jawne korekty + pobieranie przed decyzją.** Obaj agenci powinni używać identycznego kontraktu, schematu i limitów, ale osobnych prywatnych pamięci. Wspólne lekcje muszą być jawnie udostępnione. Bieżąca odpowiedź drugiego agenta nie trafia do niezależnego sprawdzenia przed złożeniem własnej oceny.

**MemRL i nagrody: shadow mode.** Obliczać oceny, pokazywać jak zmieniłyby wybór, lecz początkowo nie używać ich do sterowania zadaniami. Nie dodawać kar za brak odpowiedzi upstreamu, statystyk aktywności ani odczuwanego zmęczenia jako celu.

Proponowany kolejny etap: 20 nowych porównywalnych decyzji obu agentów, jako pilotaż wykonalności, nie wystarczający test statystyczny. Zachować ten sam model, budżet i bazowe instrukcje; porównywać aktualny proces z pamięcią oraz pamięć z Q. Przy replay stosować rozłączne nowe konteksty; przy rzeczywistych zadaniach losować warunek w obrębie agenta i typu zadania, bez duplikowania kontaktu z upstreamem. Oceny powinien sprawdzać recenzent nieznający wariantu, według kryteriów ustalonych przed zadaniem. Liczyć poprawność decyzji, powtarzanie znanych błędów, wykonane użyteczne kroki i cały koszt. Ekstrakcję lekcji oceniać osobno (czy wniosek jest poparty dowodem i ma właściwy zakres). Włączyć Q do sterowania dopiero po wykazaniu przewagi ponad samą pamięć i braku regresji bezpieczeństwa/procesu.

Prompt wdrażający dla obu agentów powinien dotyczyć właśnie tego ograniczonego zakresu. POC nie uzasadnia deklaracji „agenci już uczą się lepiej” ani włączenia pełnego autonomicznego systemu nagród.

## Ślad 20 przypadków — lexical

| Przypadek | Wskazane wcześniejsze lekcje | Przywołane karty | Hit |
|---|---|---|---|
{details}
'''
(p/'REPORT.md').write_text(text)
