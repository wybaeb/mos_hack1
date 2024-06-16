# Mos Hack Project

## Description
This project is designed to assist with purchases, create charts, and predict purchases. The bot interacts with users via Telegram and uses various modules to process and respond to user queries.

## Features
- **Purchase Assistance**: Helps users in making purchases by asking for item details and quantity.
- **Chart Creation**: (Feature to be implemented)
- **Purchase Prediction**: (Feature to be implemented)

## Project Structure
```
.
├── Dockerfile
├── main.py
├── scenario.py
├── test_api.py
├── bot2.py
├── generators.py
├── requirements.txt
├── telegram_bot.py
├── upload.ipynb
├── visualisation.ipynb
└── moshack_dump.sql
```

## Setup and Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/wybaeb/mos_hack1.git
    cd mos_hack1
    ```

2. **Create a virtual environment**:
    ```sh
    python3 -m venv rubert_env
    source rubert_env/bin/activate
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set environment variables**:
    Update the `Dockerfile` with your specific environment variables. Example:
    ```dockerfile
    ENV POSTGRES_DB=moshack
    ENV POSTGRES_USER=dbadmin
    ENV POSTGRES_PASSWORD=secret
    ENV POSTGRES_HOST=10.0.0.7
    ENV POSTGRES_PORT=30012
    ENV TELEGRAM_TOKEN=your_telegram_token
    ENV LLAMA_API_URL=http://127.0.0.1:5001
    ENV LLAMA_API_ACCESS_TOKEN=your_secure_token
    ENV DATABASE_URL=secret
    ENV LOCALE=ru
    ```

5. **Run the application**:
    ```sh
    python main.py
    ```

## Docker

1. **Build the Docker image**:
    ```sh
    docker build --platform linux/amd64 -t your_image_name .
    ```

2. **Run the Docker container**:
    ```sh
    docker run -d -p 8000:8000 --name your_container_name your_image_name
    ```

## Database

1. **Dump the database**:
    ```sh
    pg_dump -h 10.0.0.7 -p 30012 -U dbadmin -W moshack > moshack_dump.sql
    ```

2. **Restore the database**:
    ```sh
    psql -h 10.0.0.7 -p 30012 -U dbadmin -d moshack -W < moshack_dump.sql
    ```

## Usage

### Interact with the Bot

- Start the bot by sending `/start` command.
- Follow the prompts to make purchases, and enter the details as requested by the bot.




