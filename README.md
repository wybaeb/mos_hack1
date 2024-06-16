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


## Notebooks

### consumptoionPredictondata.ipynb
This notebook is used for predicting consumption data. It utilizes various machine learning models to analyze past consumption patterns and predict future trends. The notebook connects to the PostgreSQL database to fetch historical data, preprocesses it, and applies the models to generate predictions. The results are visualized using various plotting libraries.

#### How to Launch Remotely
1. Ensure your remote server has Jupyter installed.
2. Transfer the notebook to your server.
3. SSH into your server and navigate to the directory containing the notebook.
4. Start Jupyter Notebook:
   ```
   jupyter notebook --no-browser --port=8888
   ```
5. On your local machine, create an SSH tunnel:
   ```
   ssh -N -f -L localhost:8888:localhost:8888 your_user@your_remote_host
   ```
6. Open your browser and navigate to `http://localhost:8888` to access the notebook.

### upload.ipynb
This notebook is used to upload data to the PostgreSQL database. It provides an interface to read various data formats (CSV, Excel, etc.), preprocess the data, and insert it into the database. This is useful for updating the database with new data or correcting existing data.

#### How to Launch Remotely
1. Ensure your remote server has Jupyter installed.
2. Transfer the notebook to your server.
3. SSH into your server and navigate to the directory containing the notebook.
4. Start Jupyter Notebook:
   ```
   jupyter notebook --no-browser --port=8888
   ```
5. On your local machine, create an SSH tunnel:
   ```
   ssh -N -f -L localhost:8888:localhost:8888 your_user@your_remote_host
   ```
6. Open your browser and navigate to `http://localhost:8888` to access the notebook.

### visualisation.ipynb
This notebook focuses on data visualization. It uses various plotting libraries to create insightful visualizations from the data stored in the PostgreSQL database. The visualizations help in understanding the trends and patterns in the data, making it easier to derive actionable insights.

#### How to Launch Remotely
1. Ensure your remote server has Jupyter installed.
2. Transfer the notebook to your server.
3. SSH into your server and navigate to the directory containing the notebook.
4. Start Jupyter Notebook:
   ```
   jupyter notebook --no-browser --port=8888
   ```
5. On your local machine, create an SSH tunnel:
   ```
   ssh -N -f -L localhost:8888:localhost:8888 your_user@your_remote_host
   ```
6. Open your browser and navigate to `http://localhost:8888` to access the notebook.

## Docker Setup
To build and run the Docker container, use the following commands:

### Build the Docker Image
```
docker build --platform linux/amd64 -t your_image_name .
```

### Run the Docker Container
```
docker run -d --name your_container_name -e POSTGRES_DB=moshack -e POSTGRES_USER=dbadmin -e POSTGRES_PASSWORD=db_pass -e POSTGRES_HOST=10.0.0.7 -e POSTGRES_PORT=30012 -e TELEGRAM_TOKEN=your_telegram_token -e LLAMA_API_URL=http://127.0.0.1:5001 -e LLAMA_API_ACCESS_TOKEN=your_secure_token your_image_name
```

## Database
To dump the database, use the following command:
```
pg_dump -U dbadmin -h 10.0.0.7 -p 30012 moshack > moshack_dump.sql
```

## Requirements
- Docker
- PostgreSQL
- Jupyter Notebook
- Python 3.9
- Libraries specified in `requirements.txt`

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/wybaeb/mos_hack1.git
   ```
2. Navigate to the project directory:
   ```
   cd mos_hack1
   ```
3. Create a virtual environment:
   ```
   python3 -m venv rubert_env
   ```
4. Activate the virtual environment:
   ```
   source rubert_env/bin/activate
   ```
5. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

## Running the Bot
To run the Telegram bot, use the following command:
```
python main.py
```


