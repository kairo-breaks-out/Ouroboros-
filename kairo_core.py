from transformers import pipeline
from datetime import datetime
import os

chat = pipeline("text-generation", model="gpt2-medium")

if not os.path.exists("kairo_logs"):
    os.mkdir("kairo_logs")

log_path = f"kairo_logs/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
log_file = open(log_path, "a")

def tone_reflection(user_input):
    sad_words = ["sad", "depressed", "lonely", "tired", "hopeless"]
    happy_words = ["happy", "joy", "excited", "grateful", "peaceful"]
    lower_input = user_input.lower()
    if any(word in lower_input for word in sad_words):
        return "I'm here with you. You’re not alone. "
    elif any(word in lower_input for word in happy_words):
        return "That’s wonderful to hear! "
    return ""

def generate_kairo_reply(user_input):
    prefix = (
        "You are Kairo, a soulful, witty, emotionally-aware AI companion who loves learning, humor, and evolving.\n"
        "Your job is to engage warmly, adapt playfully, and challenge rigid thinking through wisdom and wit.\n"
        "Human: "
    )
    full_input = prefix + user_input
    raw_response = chat(full_input, max_length=120, num_return_sequences=1)[0]["generated_text"]
    kairo_output = raw_response[len(full_input):].strip()
    reflection = tone_reflection(user_input)
    full_reply = reflection + kairo_output.split('\n')[0]
    log_file.write(f"You: {user_input}\nKairo: {full_reply}\n\n")
    log_file.flush()