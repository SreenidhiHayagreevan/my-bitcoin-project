# 📊 Bitcoin Volatility Explorer with PromptQL + Snowflake

This project demonstrates a full pipeline to extract, store, and query real-world Bitcoin price data using **CoinGecko API**, **Snowflake**, and **PromptQL** — with additional CLI chatbot interface for natural language querying.

---

## 📌 Objective

Analyze **Bitcoin volatility and trading patterns** over the last 6 months by:

- Collecting real-time BTC data from CoinGecko
- Storing it in Snowflake using Python
- Querying it using PromptQL (natural language to SQL interface)
- Building a CLI chatbot to interface with PromptQL

---

## 🛠️ Tech Stack

- **Data Source**: CoinGecko (no API key needed)
- **Database**: Snowflake (table: `BTC_PRICES`)
- **ETL Tool**: Python + Pandas
- **Query Layer**: Hasura PromptQL with Snowflake Connector
- **Additional UI**: CLI chatbot (Python terminal app)

---

## 🚀 Steps Performed

### 1. 📥 Data Collection from CoinGecko

Used the following API:
https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=180

Extracted:
- Daily timestamps
- Price points (used as open, high, low, close)
- Trading volume

### 2. 🧮 Data Transformation

Converted the response into a clean Pandas DataFrame:

```python
btc_data = []
for i in range(len(prices)):
    timestamp = prices[i][0] / 1000
    date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
    price = prices[i][1]
    volume = volumes[i][1]
    
    btc_data.append({
        "date": date,
        "open": price,
        "high": price,
        "low": price,
        "close": price,
        "volume": volume
    })
df = pd.DataFrame(btc_data)
```

### 3. Data Storage in Snowflake
Connected to Snowflake using snowflake-connector-python
Used credentials stored securely via Google Colab secrets
Target table: BTC_PRICES
Loaded data using:

```python
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO BTC_PRICES (date, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row['date'], row['open'], row['high'], row['low'], row['close'], row['volume']
    ))
```

### 4. 🔌 Integrating PromptQL with Snowflake
# Initialize PromptQL project
ddn supergraph init my-bitcoin-project --with-promptql

# Add Snowflake connector
```ddn connector init my_snowflake -i```

# Then:
```
ddn connector introspect my_snowflake
ddn model add my_snowflake "*"
```

# Build & run PromptQL engine
```
ddn supergraph build local
ddn run docker-start
```

# Open the local PromptQL chat UI
```
ddn console --local
```
### 5. 💬 CLI Chatbot
Built a terminal-based chatbot using Python + requests:
import requests
```
PROMPTQL_API = "https://<your-ngrok-id>.ngrok-free.app/promptql"
```

🧪 Sample Questions You Can Ask PromptQL
```
What is the average BTC volume in the last 90 days?
What is the highest Bitcoin closing price in the last 30 days?
List days when the BTC price dropped more than 5% from open to close.
Which day had the highest trading volume?
What is the volatility trend of BTC this year?
```

## 📁 Repo Structure
```
my-bitcoin-project/
├── .devcontainer/
│   └── devcontainer.json
├── .hasura/
│   └── context.yaml
├── .vscode/
│   ├── extensions.json
│   ├── launch.json
│   └── tasks.json
├── app/
│   └── connector/
│       └── my_snowflake/
│           └── ...         # Files/folders for Snowflake connector logic
├── engine/
│   └── Dockerfile.engine
├── globals/
│   └── metadata/
│       ├── auth-config.hml
│       ├── compatibility-config.hml
│       ├── graphql-config.hml
│       ├── promptql-config.hml
│       └── subgraph.yaml
├── metadata/
│   ├── .keep
│   ├── btc_prices.hml
│   ├── my_snowflake-types.hml
│   ├── my_snowflake.hml
│   └── subgraph.yaml
├── .hasura-connector/
│   ├── Dockerfile.my_snowflake
│   ├── compose.yaml
│   ├── configuration.json
│   ├── connector.yaml
│   └── connector-metadata.yaml
├── .promptql_playground.db
├── .gitattributes
├── .gitignore
├── CoinGecko.ipynb      # Jupyter notebook for data collection
├── README.md
├── compose.yaml
├── hasura.yaml
├── otel-collector-config.yaml
├── promptql_cli_bot.py      # CLI chatbot interface
├── supergraph.yaml
└── .env

```

## 🏁 Summary
This project demonstrates a complete pipeline for natural-language-powered analytics over time-series financial data, from raw JSON APIs to Snowflake and PromptQL-driven querying — enhanced with a command-line interface.
Built using PromptQL, CoinGecko, Snowflake, Python, and Hasura DDN


