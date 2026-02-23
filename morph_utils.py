import pymorphy3
from functools import lru_cache
from data import PLACES as DATA_PLACES

morph = pymorphy3.MorphAnalyzer()


# ---------------------------
# КЭШ ДЛЯ УСКОРЕНИЯ
# ---------------------------

@lru_cache(maxsize=1000)
def parse_word(word: str):
    """Кэшированный разбор слова"""
    return morph.parse(word)[0]


# ---------------------------
# ПРЕДЛОГИ ДЛЯ МЕСТ
# ---------------------------

PLACES_WITH_PREP = {
    'холодильник': ('в', 'холодильнике'),
    'университет': ('в', 'университете'),
    'космос': ('в', 'космосе'),
    'шкаф': ('в', 'шкафу'),
    'кофейня': ('в', 'кофейне'),
    'библиотека': ('в', 'библиотеке'),
    'ванна': ('в', 'ванне'),
    'интернет': ('в', 'интернете'),
    'лифт': ('в', 'лифте'),
    'парк': ('в', 'парке'),
    'кинотеатр': ('в', 'кинотеатре'),
    'супермаркет': ('в', 'супермаркете'),
    'стадион': ('на', 'стадионе'),
    'музей': ('в', 'музее'),
    'пляж': ('на', 'пляже'),
    'самолёт': ('в', 'самолёте'),
    'поезд': ('в', 'поезде'),
    'метро': ('в', 'метро'),
    'автобус': ('в', 'автобусе'),
    'такси': ('в', 'такси'),
    'пещера': ('в', 'пещере'),
    'замок': ('в', 'замке'),
    'небоскрёб': ('в', 'небоскрёбе'),
    'подвал': ('в', 'подвале'),
    'чердак': ('на', 'чердаке'),
    'сарай': ('в', 'сарае'),
    'гараж': ('в', 'гараже'),
    'аквапарк': ('в', 'аквапарке'),
    'зоопарк': ('в', 'зоопарке'),
    'планетарий': ('в', 'планетарии'),
    'горка': ('на', 'горке'),
    'карусель': ('на', 'карусели'),
    'эскалатор': ('на', 'эскалаторе'),
    'площадь': ('на', 'площади'),
    'улица': ('на', 'улице'),
    'остров': ('на', 'острове'),
    'гора': ('на', 'горе'),
    'лес': ('в', 'лесу'),
    'сад': ('в', 'саду'),
    'берег': ('на', 'берегу'),
    'река': ('на', 'реке'),
    'озеро': ('на', 'озере'),
    'поле': ('на', 'поле'),
    'пустыня': ('в', 'пустыне'),
}


def get_place_with_preposition(place: str):
    """Возвращает правильный предлог и форму места"""

    place_lower = place.lower()

    if place_lower in PLACES_WITH_PREP:
        return PLACES_WITH_PREP[place_lower]

    # Фоллбэк через pymorphy3
    parsed = parse_word(place_lower)
    inflected = parsed.inflect({'loct'})
    place_form = inflected.word if inflected else place_lower

    return 'в', place_form


# ---------------------------
# ОСНОВНАЯ ФУНКЦИЯ
# ---------------------------

def make_sentence(noun: str, verb: str, adjective: str, place: str):
    """Собирает грамматически корректное предложение"""

    # 1️⃣ Существительное
    noun_parsed = parse_word(noun)
    gender = noun_parsed.tag.gender or 'masc'

    noun_inflected = noun_parsed.inflect({'nomn'})
    noun_word = noun_inflected.word if noun_inflected else noun

    # 2️⃣ Прилагательное
    adj_parsed = parse_word(adjective)
    adj_inflected = adj_parsed.inflect({gender, 'nomn'})
    adj_word = adj_inflected.word if adj_inflected else adjective

    # 3️⃣ Глагол в прошедшем времени через pymorphy3
    verb_parsed = parse_word(verb)
    verb_inflected = verb_parsed.inflect({'past', gender})

    if verb_inflected:
        verb_word = verb_inflected.word
    else:
        verb_word = verb

    # 4️⃣ Место
    preposition, place_word = get_place_with_preposition(place)

    # 5️⃣ Финальная сборка
    return f"{adj_word.capitalize()} {noun_word} {verb_word} {preposition} {place_word}."