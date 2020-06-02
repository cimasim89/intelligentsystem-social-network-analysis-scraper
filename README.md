# Social Network Analysis - Scraper.py

Questo script e' parte del progetto didattico universitario "Social Network Analysis" di Intelligent System.

### Disclaimer
Questo progetto didattico utilizza dei dati presi dal sito Repubblica, i dati vengono utilizzati per crearne un grafo di parole connesse relativo alle parole presenti nel titolo degli articoli. Nessun dato verra' utilizzato per scopi ludici dall'autore. Non ci si assume la responsabilita' di usi illeciti.

### Operazioni preliminari
Installare le dipendenze del progetto indicate nel file `requirements.txt`

```shell script
$ pip install -r requirements.txt 
```

### Scraper.py
Scraper.py permette di effettuare lo scraping della pagina html di repubblica per recuperare i dati necessari per l'esercitazione.

Per utilizzare lo script Scraper.py e' necessario scaricare il driver relativo al proprio browser.

E' possibile reperire il driver per Google Chrome all'indirizzo https://chromedriver.chromium.org

#### Parametri
I parametri possono essere passati come argomento, altrimenti verrano richiesti all'inizio dell'esecuzione.

- `--driver-path: string` path del driver 
- `--result-filename: string ` nome del file di destinazione
- `--query: string` query di ricerca
- `--pages: int` limite di pagine da ricercare
- `--start-date: string` data di inizio ricerca `formato: YYYY-MM-DD`
- `--end-date: string` data di fine ricerca `formato: YYYY-MM-DD`


#### Esempio
```shell script
$ python Scraper.py \
--driver-path=./chromedriver \
--result-filename=result.json 
--query=Spoleto \
--pages=100 \
--start-date=2020-01-01 \
--end-date=2020-02-01
```

