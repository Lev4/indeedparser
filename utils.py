import time
import sys

class Vacancy:

    def __init__(self, vacancy_id, vacancy_description, profession, country, city, requirements, skills, parsing_date):
        self.vacancy_id = vacancy_id,
        self.vacancy_description =  vacancy_description,
        self.profession = profession
        self.country = country,
        self.city = city,
        self.requirements = requirements,
        self.skills = skills,
        self.parsing_date = parsing_date



def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round((ended_at - started_at) / 60, 1)

        print(f'Функция работала {elapsed} минут(ы)')
        return result

    return surrogate

def get_location_from_args():
    """ Возвращает город из аргуметна командной строки"""

    location_args = sys.argv
    space_lock_join = None

    if len(location_args) > 1:
        if len(location_args[1].split("_")) > 1:
            space_lock_join = ' '.join(location_args[1].split("_"))
            print(space_lock_join)
        else:
            space_lock_join = location_args[1]

    return space_lock_join





professions_ru = [
    "Java разработчик ",
    "Software engineer",
    "Web разработчик",
    "Front-end разработчик",
    "Продуктовый дизайнер",
    "Системный аналитик",
    "Архитектор систем",
    "Agile coach",
    "Data Scientist",
    "Data engineer",
    "Бизнес-аналитик",
    "Финансовый аналитик",
    "Кредитный аналитик",
    "Юрист корпоративный",
    "Юрист судебный",
    "Маркетолог",
]

professions_en = [
    "Java Developer ",
    "Software engineer",
    "Web Developer",
    "Front-end Developer",
    "Product Designer",
    "System analyst",
    "System architect",
    "Agile coach",
    "Data Scientist",
    "Data engineer",
    "Business-analyst",
    "Financial analyst",
    "Credit analyst",
    "Corporate lawyer",
    "Judicial Lawyer",
    "Marketing Manager",
    "Marketing Specialist",
]

professions = {
    "ru": professions_ru,
    "en": professions_en,
}

regions = {
    "us": ["Texas", "New York", "Dallas", "California", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana",
           "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
           "Minnesota"],
    "de": ["Germany", "Berlin"],
    "uk": ["London", "Edinburgh", "Manchester", "Birmingham", "Leeds", "Glasgow", "Southampton", "Liverpool",
           "Newcastle", "Nottingham", "Sheffield", "Bristol", "Belfast", "Leicester"],
    "ru": ["Москва", "Moscow"]
}

patterns_dict = {
    "Requirements": [
        {"LEMMA": "requirements"},
        {"IS_PUNCT": True, "OP": "?"},
    ],

    "Required Skills": [
        {"LOWER": "require", },
        {"LOWER": "skill"}
    ],
    "Experience & Skills Required": [
        {"LEMMA": "experience", "LOWER": "experience"},
        {"IS_PUNCT": True, "OP": "?"},
        {"LEMMA": "skill"},
        {"LEMMA": "require"}
    ],
    "Essential Knowledge, Skills and Experience Required": [
        {"LEMMA": "essential",
         "LOWER": "essential",
         "OP": "?"
         },
        {"IS_PUNCT": True, "OP": "?"},
        {
            "LEMMA": "knowledge",
            "LOWER": "knowledge",
            "OP": "?"
        },
        {"LEMMA": "skill", "LOWER": "skill"},
        {"LEMMA": "experience", "LOWER": "experience"},
        {"LEMMA": "require", "LOWER": "require"},
    ],

    "Desirable Experience": [
        {"LEMMA": "desire"},
        {"LEMMA": "experience"},
    ],
    "The ideal candidate": [
        {"LEMMA": "ideal"},
        {"LEMMA": "candidate"},
    ],
    "REQUIRED SKILLS AND KNOWLEDGE": [
        {"LEMMA": "require"},
        {"LEMMA": "skill"},
        {"LEMMA": "and"},
        {"LEMMA": "knowledge"},
    ],
    "YOUR SKILLS AND EXPERIENCE": [
        {"LEMMA": "you"},
        {"LEMMA": "skill"},
        {"LEMMA": "and"},
        {"LEMMA": "experience"},
    ],
    "Key Requirements:": [
        {"LEMMA": "key"},
        {"LEMMA": "requirement"},
    ],
    "You'll need to have:": [
        {"LEMMA": "need"},
        {"TEXT": "to"},
        {"LEMMA": "have"},
        {"IS_PUNCT": True, "OP": "?"},
    ],

    "Qualifications:": [
        {"LEMMA": "qualification", "LOWER": "qualification"},
        {"IS_PUNCT": True, "OP": "?"},
    ],
    "If you have a": [
        {"LEMMA": "you"},
        {"LEMMA": "have"},
    ],
    "Why you?": [
        {"LEMMA": "why"},
        {"LEMMA": "you"},
        {"IS_PUNCT": True, "OP": "?"},
    ],
    "Basic Qualifications:": [
        {"LEMMA": "basic"},
        {"LEMMA": "qualification"},
    ],
    "Preferred Qualifications:": [
        {"LEMMA": "prefer"},
        {"LEMMA": "qualification"},
    ],
    "successful candidate will have": [
        {"LEMMA": "success"},
        {"LEMMA": "candidate"},
        {"LEMMA": "will", "OP": "?"},
        {"LEMMA": "have"},
    ],
    "WHAT SKILLS YOU’LL NEED": [
        {"LEMMA": "what"},
        {"LEMMA": "skill"},
        {"LEMMA": "you"},
        {"LEMMA": "need"},
    ],
    "YOUR SKILLS & EXPERIENCE": [
        {"LEMMA": "you"},
        {"LEMMA": "skill"},
        {"IS_PUNCT": True, "OP": "?"},
        {"LEMMA": "experience"},
    ],
    "You must have": [
        {"LEMMA": "you"},
        {"LEMMA": "must", "OP": "?"},
        {"LEMMA": "have"},

    ],

    "About you:": [
        {"LEMMA": "about"},
        {"LEMMA": "you"},
    ],

    "WHAT SKILLS YOU'LL NEED": [
        {"TEXT": "what", "LOWER": "what"},
        {"LEMMA": "skill", "LOWER": "skill"},
        {"LEMMA": "you", "LOWER": "you"},
        {"LEMMA": "will", "OP": "?"},
        {"LEMMA": "need", "LOWER": "need"},
    ],

    "Ideally, you’ll": [
        {"LEMMA": "ideal", "LOWER": "ideal"},
        {"LEMMA": "you"},
    ],
    "Desirable at entry:": [
        {"LEMMA": "desire"},
        {"TEXT": "at"},
        {"LEMMA": "entrance"},
    ],
    "Nice to have": [
        {"LEMMA": "nice"},
        {"TEXT": "to"},
        {"LEMMA": "have"},
    ]
}
