import time


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'Функция работала {elapsed} секунд(ы)')
        return result

    return surrogate


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
    "uk": ["London", "Edinburgh"],
    "ru": ["Москва", "Moscow"]
}
