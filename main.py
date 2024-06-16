import os
import re
import pandas as pd
import psycopg2
import torch
from transformers import AutoTokenizer, AutoModel
from dotenv import load_dotenv
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
from scenario import scenario
from generators import *

# Load environment variables from .env file
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

CHOOSING, TYPING_REPLY = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['dialogHistory'] = []
    context.user_data['answersData'] = []
    await send_scenario_step(update, context, "1")
    return CHOOSING

async def send_scenario_step(update: Update, context: ContextTypes.DEFAULT_TYPE, step_id: str) -> None:
    step = next(item for item in scenario if item["stepId"] == step_id)
    context.user_data['dialogHistory'].append(step_id)

    answers = generate_answers(step, "", context.user_data['dialogHistory'], context.user_data['answersData'], context)
    question_with_postfix = apply_template(append_postfix(step['question'], answers), context)

    reply_markup = ReplyKeyboardMarkup([[answer['answerText'] for answer in answers]], one_time_keyboard=True)
    await update.message.reply_text(question_with_postfix, reply_markup=reply_markup)

def apply_template(template: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    for key, value in context.user_data.items():
        if isinstance(value, str):
            template = template.replace(f"${{{key}}}", value)
    return template

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text
    current_step_id = context.user_data['dialogHistory'][-1]
    current_step = next(item for item in scenario if item["stepId"] == current_step_id)

    # Generate current step answers
    current_answers = generate_answers(current_step, user_text, context.user_data['dialogHistory'], context.user_data['answersData'], context)
    current_answer_map = {answer['answerText']: answer['answerId'] for answer in current_answers}

    # Collect all previous answers
    previous_answers = {
        answer['answerText']: answer['answerId']
        for answer in context.user_data['answersData']
    }
    
    # Combine current and previous answers
    answer_map = {**previous_answers, **current_answer_map}

    # Determine if user_text matches any answerText
    if user_text in answer_map:
        answer_id = answer_map[user_text]
    else:
        answer_id = None

    # Store user answer
    context.user_data['answersData'].append({
        "stepId": current_step_id,
        "answerText": user_text,
        "answerId": answer_id
    })

    # Let generators handle context updates
    update_context_variables(current_step_id, user_text, context)

    # Determine next step
    if answer_id and answer_id in current_step["jumpTo"]:
        next_step_id = current_step["jumpTo"][answer_id]
    else:
        next_step_id = "intentNotImplemented"

    await send_scenario_step(update, context, next_step_id)
    return CHOOSING

def generate_answers(step, textAnswer, dialogHistory, answersData, context):
    function_name = step["answersGenerator"]
    return globals()[function_name](textAnswer, dialogHistory, answersData, context)

def append_postfix(question, answers):
    if not answers:
        return question
    return f"{question} {answers[-1]['answerText']}"

def main():
    # Create the application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add conversation handler with states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
