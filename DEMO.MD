# DEMO Proteus

Questa guida e pensata per una demo live (10-15 minuti) in cui fai vedere:
- cosa fa Proteus
- come si usa
- cosa succede dietro le quinte

Il taglio e pratico: puoi leggerla mentre presenti e copiare i blocchi di codice cosi come sono.

---

## 1. Obiettivo della demo

Mostrare che Proteus permette di:
1. caricare configurazioni da file diversi (`.yaml`, `.json`, `.env`)
2. leggere valori con una API unica (`get("path.dot")`)
3. fare merge profondo di configurazioni (`load` + `merge`)
4. tradurre automaticamente tra formati (`translate`)
5. mantenere un design pulito ed estendibile (pattern: Facade, Factory Method, Template Method, Adapter, singleton opzionale)

---

## 2. Prerequisiti

Da root progetto (`C:\Users\lucad\my-projects\proteus`):

```powershell
& .\.venv\Scripts\Activate.ps1
pip install -e .
```

Se vuoi verificare rapidamente che tutto e ok:

```powershell
python -m pytest -q
```

---

## 3. Mini mappa mentale (prima di iniziare)

Quando chiami `ConfigurationManager.load("file.yaml")`, internamente succede questo:

1. `ConfigurationManager` (Facade) riceve la richiesta
2. legge l'estensione (`.yaml`) e sceglie il `FormatCreator` giusto
3. il `FormatCreator` crea un `Reader` del formato corretto
4. il `Reader` esegue il Template Method: valida file, legge testo, parse
5. il parse vero lo fa l'`Adapter` (es. `YAMLAdapter` con `yaml.safe_load`)
6. il manager fa deep-merge nel dizionario interno `_config`

Risultato: API semplice per chi usa la libreria, complessita incapsulata dentro.

---

## 4. Demo guidata (copione completo)

## Step 1 - Caricamento base e lettura chiavi

### Cosa fai in demo

Esegui:

```powershell
python examples\basic_usage.py
```

### Cosa vedra il pubblico

- lettura di `config_examples/app.yaml`
- accesso a chiavi semplici e annidate
- uso di default su chiave mancante

Esempi output atteso (semplificato):

```text
App name : proteus-demo
DB host  : localhost
DB port  : 5432
Log level: INFO
Timeout  : 30
```

### Dietro le quinte

- `config.load("config_examples/app.yaml")`
  - estensione `.yaml` -> `YAMLFormatCreator`
  - `YAMLFormatCreator.create_reader()` -> `YAMLReader`
  - `YAMLReader.parse()`:
    - `_validate()` verifica che il file esista
    - `_read_file()` legge il contenuto UTF-8
    - `_parse_content()` delega a `YAMLAdapter.load()`
- `YAMLAdapter.load()` usa `yaml.safe_load()` e restituisce un `dict`
- il manager fonde il risultato in `_config`
- `get("database.host")` percorre il dict per segmenti separati da `.`

---

## Step 2 - Merge tra config base e production

### Cosa fai in demo

Esegui:

```powershell
python examples\merge_configs.py
```

### Cosa vedra il pubblico

Prima viene caricato `app.yaml`, poi `production.yaml` viene applicato sopra.

Aspettative chiave:
- `database.host` cambia da `localhost` a `prod-db.example.com`
- `database.port` resta `5432` (non sovrascritto)
- `logging.level` cambia da `INFO` a `WARNING`

### Dietro le quinte

- `merge()` e un alias semantico di `load()`
- la parte critica e `_deep_merge(base, override)`:
  - se valore base e override sono entrambi `dict`, merge ricorsivo
  - altrimenti vince `override`
- in pratica ottieni layering di configurazioni (base -> env specific)

Questo e il caso d'uso piu comune in produzione.

---

## Step 3 - Traduzione tra formati

### Cosa fai in demo

Esegui:

```powershell
python examples\translate.py
```

Lo script mostra:
1. YAML -> JSON
2. JSON -> ENV
3. ENV -> YAML

I file vengono creati in `config_examples/output/`.

### Cosa vedra il pubblico

La stessa configurazione viene rappresentata in formati diversi mantenendo il contenuto logico.

Esempio: in ENV le strutture annidate diventano chiavi flat con `__`:

```text
DATABASE__HOST=localhost
DATABASE__PORT=5432
```

### Dietro le quinte

- `translate(input_path, output_path)`:
  - prende creator input in base all'estensione sorgente
  - prende creator output in base all'estensione destinazione
  - `reader.parse(input)` -> ottieni dict interno (IR)
  - `writer.write(data, output)` -> serializza nel formato target
- in ENV adapter:
  - `dump()` fa flatten dei nested dict (`A.B.C` -> `A__B__C`)
  - converte valori in stringa e aggiunge virgolette quando servono

Messaggio importante in demo: **Proteus lavora su una rappresentazione intermedia a dizionario**, quindi il passaggio tra formati e naturale.

---

## Step 4 - Mostrare l'API in 30 secondi (snippet live)

Se vuoi una mini demo live in terminale:

```python
from proteus import ConfigurationManager

cfg = ConfigurationManager()
cfg.load("config_examples/app.yaml")
cfg.merge("config_examples/production.yaml")

print(cfg.get("database.host"))      # prod-db.example.com
print(cfg.get("database.port"))      # 5432
print(cfg.get("server.timeout", 30)) # default

cfg.translate("config_examples/app.yaml", "config_examples/output/demo.json")
print(cfg.loaded_files())
```

Se la esegui in REPL Python, spiega queste 3 idee:
- API minima
- merge profondo
- conversione formati

---

## 5. Come raccontare i pattern senza appesantire la demo

Testo breve da dire a voce:

- **Facade**: io chiamo pochi metodi semplici (`load/get/merge/translate`)
- **Factory Method**: la libreria sceglie da sola il reader/writer giusto
- **Template Method**: tutti i reader/writer seguono la stessa pipeline
- **Adapter**: parsing/serializzazione delegati a librerie esterne in modo isolato
- **Singleton opzionale**: un manager condiviso solo quando lo richiedi con `ConfigurationManager.instance()`

Suggerimento pratico: non entrare subito nei nomi delle classi. Parti dal valore per l'utente, poi mappa ai pattern.

---

## 6. Problemi comuni durante la demo (e soluzione rapida)

1. `FileNotFoundError`
- Causa: comando lanciato fuori dalla root progetto
- Fix: spostati in `C:\Users\lucad\my-projects\proteus`

2. `UnsupportedFormatError`
- Causa: estensione non registrata
- Fix: usa `.yaml`, `.yml`, `.json`, `.env`

3. `ConfigurationNotLoadedError`
- Causa: chiamata `get()` prima di `load()`
- Fix: carica almeno un file prima di leggere chiavi

4. output ENV con chiavi uppercase e `__`
- Causa: comportamento voluto dell'`EnvAdapter`
- Fix: spiega che e la normalizzazione standard per nested data in ENV

---

## 7. Demo script ultra-breve (3 minuti)

Se hai poco tempo, usa questo ordine:

1. `python examples\basic_usage.py`
2. `python examples\merge_configs.py`
3. `python examples\translate.py`

Frase di chiusura consigliata:

"Con una sola API posso caricare, unire e convertire configurazioni in formati diversi, mantenendo il codice applicativo pulito e indipendente dai dettagli di parsing."

---

## 8. Extra: cosa mostrare se ti fanno domande tecniche

- Test suite: `python -m pytest -q` (copertura molto alta)
- Estendibilita: `register_creator()` permette nuovi formati senza toccare codice esistente
- Sicurezza YAML: uso di `yaml.safe_load()`
- Dot notation: accesso a chiavi annidate con fallback default

---

Fine demo.
