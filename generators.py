import re
import os
import psycopg2
import torch
from transformers import AutoTokenizer, AutoModel
from dotenv import load_dotenv
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Load environment variables from .env file
load_dotenv()
db_name = os.getenv('DB_NAME', 'moshack')
db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'postgres')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')

# Initialize the ruBert model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")
model = AutoModel.from_pretrained("DeepPavlov/rubert-base-cased")

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

def find_most_similar(text, top_n=5):
    input_embedding = get_embedding(text)
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    df = pd.read_sql("SELECT nazvanie_ste, embedding FROM dictionary WHERE embedding IS NOT NULL;", conn)
    embeddings = [pickle.loads(row['embedding']) for index, row in df.iterrows()]
    distances = [np.linalg.norm(input_embedding - e) for e in embeddings]
    df['embedding_distance'] = distances
    top_embedding_similar = df.nsmallest(top_n, 'embedding_distance')
    vectorizer = TfidfVectorizer().fit(df['nazvanie_ste'])
    tfidf_matrix = vectorizer.transform(df['nazvanie_ste'])
    query_vector = vectorizer.transform([text])
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    df['text_similarity'] = cosine_similarities
    top_text_similar = df.nlargest(top_n, 'text_similarity')
    combined_top = pd.concat([top_embedding_similar, top_text_similar]).drop_duplicates().nlargest(top_n, ['embedding_distance', 'text_similarity'])
    conn.close()
    return combined_top['nazvanie_ste'].tolist()

def intentAnswers(textAnswer, dialogHistory, answersData, context):
    return [
        {"answerId": "make_Purchase", "answerText": "Сделать покупку"},
        {"answerId": "draw_Diagram", "answerText": "Создать диаграмму"},
        {"answerId": "predict_Purchase", "answerText": "Прогнозировать покупку"}
    ]

def getAssetName(textAnswer, dialogHistory, answersData, context):
    if textAnswer:
        most_similar_items = find_most_similar(textAnswer, top_n=5)
        return [{"answerId": "assetNameProvided", "answerText": item} for item in most_similar_items]
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    cur = conn.cursor()
    query = "SELECT asset_name FROM monthly_asset_analytics WHERE wave_turns_number > 2"
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"answerId": "assetNameProvided", "answerText": row[0]} for row in rows]

def stringToNumber(text):
    cleaned_text = re.sub(r'[^\d.,]', '', text)
    cleaned_text = cleaned_text.replace(',', '.')
    try:
        return int(cleaned_text)
    except ValueError:
        try:
            return float(cleaned_text)
        except ValueError:
            return None

def get_max_number(asset_name):
    query = "SELECT max_number FROM monthly_asset_analytics WHERE asset_name = %s"
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    cur = conn.cursor()
    cur.execute(query, (asset_name,))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def getAssetQuantity(textAnswer, dialogHistory, answersData, context):
    asset_name = next((answer['answerText'] for answer in answersData if answer['stepId'] == "2"), None)
    max_number = get_max_number(asset_name)
    if textAnswer:
        number = stringToNumber(textAnswer)
        if number is not None:
            return [{"answerId": "quantityProvided", "answerText": str(number)}]
    if max_number is not None:
        return [{"answerId": "quantityProvided", "answerText": str(max_number)}]
    return []

def getAssetCharacteristic(textAnswer, dialogHistory, answersData, context):
    asset_name = next((answer['answerText'] for answer in answersData if answer['stepId'] == "2"), None)
    conn = psycopg2.connect(
        dbname        = db_name,
        user = db_user,
        password = db_password,
        host = db_host,
        port = db_port
    )
    cur = conn.cursor()
    query = "SELECT naimenovanie_harakteristik FROM dictionary WHERE nazvanie_ste = %s"
    cur.execute(query, (asset_name,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        characteristics = result[0].split(';')
        return [{"answerId": f"characteristic_{i}", "answerText": char} for i, char in enumerate(characteristics)]
    return []

def getCharacteristicValue(textAnswer, dialogHistory, answersData, context):
    if textAnswer:
        return [{"answerId": "characteristicValueProvided", "answerText": textAnswer}]
    return []

def yesNoAnswers(textAnswer, dialogHistory, answersData, context):
    return [
        {"answerId": "yes", "answerText": "Да"},
        {"answerId": "no", "answerText": "Нет"}
    ]

def confirmationAnswers(textAnswer, dialogHistory, answersData, context):
    return [
        {"answerId": "yes", "answerText": "Да"},
        {"answerId": "no", "answerText": "Нет"}
    ]

def endConversation(textAnswer, dialogHistory, answersData, context):
    return []

def update_context_variables(step_id, user_text, context):
    if step_id == "2":
        context.user_data['lastAssetName'] = user_text
    elif step_id == "3":
        context.user_data['lastQuantity'] = user_text
    elif step_id == "5":
        context.user_data['lastCharacteristic'] = user_text

