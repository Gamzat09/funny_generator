from flask import Flask, render_template, jsonify
import random
from data import NOUNS, VERBS, ADJECTIVES, PLACES
from morph_utils import make_sentence

app = Flask(__name__)

counter = 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate')
def generate():
    global counter  # Используем глобальную переменную
    counter += 1  
    
    # Выбираем случайные слова
    noun = random.choice(NOUNS)
    verb = random.choice(VERBS) 
    adjective = random.choice(ADJECTIVES)
    place = random.choice(PLACES)
    
    # Создаем предложение
    sentence = make_sentence(noun, verb, adjective, place)
    
    # ДОБАВЛЯЕМ stats в ответ
    return jsonify({
        'sentence': sentence,
        'words': {
            'noun': noun,
            'verb': verb,
            'adjective': adjective,
            'place': place
        },
        'stats': {  # ← ВОТ ЭТО ОБЯЗАТЕЛЬНО!
            'total': counter,
            'combinations': len(NOUNS) * len(VERBS) * len(ADJECTIVES) * len(PLACES)
        }
    })

if __name__ == '__main__':
    print("🚀 Сервер запущен!")
    print(f"📊 Комбинаций: {len(NOUNS) * len(VERBS) * len(ADJECTIVES) * len(PLACES)}")
    app.run(debug=True, port=5000)