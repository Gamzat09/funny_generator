from flask import Flask, render_template, jsonify
import random
import threading
import os
from data import NOUNS, VERBS, ADJECTIVES, PLACES
from morph_utils import make_sentence

app = Flask(__name__)

counter = 0
counter_lock = threading.Lock() 
last_noun = None
last_verb = None
last_adjective = None
last_place = None

@app.route('/')
def home():
    return render_template('index.html')

def pick_new_word(word_list, last_word):
    word = random.choice(word_list)
    attempts = 0
    while word == last_word and attempts < 5:
        word = random.choice(word_list)
        attempts += 1
    return word

@app.route('/generate')
def generate():
    global counter
    global last_noun, last_verb, last_adjective, last_place

    with counter_lock:
        counter += 1
        current_count = counter

    noun = pick_new_word(NOUNS, last_noun)
    verb = pick_new_word(VERBS, last_verb)
    adjective = pick_new_word(ADJECTIVES, last_adjective)
    place = pick_new_word(PLACES, last_place)

    # 🎭 Умный контроль совпадения
    if noun.lower() == place.lower():
        if random.random() > 0.2:
            attempts = 0
            while place.lower() == noun.lower() and attempts < 5:
                place = random.choice(PLACES)
                attempts += 1

    # ⬇ Обновляем только после финального выбора
    last_noun = noun
    last_verb = verb
    last_adjective = adjective
    last_place = place

    try:
        sentence = make_sentence(noun, verb, adjective, place)
    except Exception as e:
        return jsonify({'error': f'Ошибка генерации: {str(e)}'}), 500

    return jsonify({
        'sentence': sentence,
        'words': {
            'noun': noun,
            'verb': verb,
            'adjective': adjective,
            'place': place
        },
        'stats': {
            'total': current_count,
            'combinations': len(NOUNS) * len(VERBS) * len(ADJECTIVES) * len(PLACES)
        }
    })


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'

    print("🚀 Основной сайт: http://localhost:5000")

    app.run(debug=debug_mode, port=5000) 