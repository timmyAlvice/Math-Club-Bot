import random
import sympy as sp
from sympy.abc import x

class TestQuestionGenerator:
    def __init__(self, num_questions):
        self.num_questions = num_questions
        self.questions = self.generate_questions()

    def generate_questions(self):
        questions = []
        num_theoretical = self.num_questions // 2
        num_practical = self.num_questions - num_theoretical

        # Теоретические вопросы
        theoretical_questions_pool = [
            {
                "question": "Что такое производная функции?",
                "answers": [
                    "Инструмент для определения угла наклона касательной к графику функции",
                    "Выражение для нахождения площади под графиком функции",
                    "Способ вычисления значения функции в любой точке",
                    "Процесс интегрирования функции"
                ],
                "correct": 0
            },
            {
                "question": "Каков геометрический смысл производной?",
                "answers": [
                    "Это площадь под графиком",
                    "Это наклон секущей линии",
                    "Это наклон касательной линии",
                    "Это длина хорды"
                ],
                "correct": 2
            },
            {
                "question": "Каков физический смысл производной?",
                "answers": [
                    "Скорость изменения функции",
                    "Положение тела в пространстве",
                    "Ускорение тела при равномерном движении",
                    "Сила, действующая на тело"
                ],
                "correct": 0
            }
        ]

        # Генерация теоретических вопросов
        questions.extend(random.sample(theoretical_questions_pool, min(num_theoretical, len(theoretical_questions_pool))))

        # Практические вопросы
        practical_formulas = [
            (sp.sin(x), "Косинус функции"),
            (sp.cos(x), "-Синус функции"),
            (sp.exp(x), "Экспонента"),
            (sp.log(x), "1/x"),
            (x**2, "2x"),
            (x**3, "3x^2"),
            (1/x, "-1/x^2"),
            (sp.sqrt(x), "1/(2*sqrt(x))")
        ]

        # Добавление практических вопросов
        cos_sin_question_included = False

        if not cos_sin_question_included:
            formula = sp.cos(x)
            derivative = sp.diff(formula, x)
            wrong_derivatives = [sp.diff(f, x) for f, _ in random.sample(practical_formulas, 3)]
            all_answers = [derivative] + wrong_derivatives
            random.shuffle(all_answers)

            practical_question = {
                "question": f"Найдите производную функции: {formula}",
                "answers": [str(ans) for ans in all_answers],
                "correct": all_answers.index(derivative)
            }

            questions.append(practical_question)
            cos_sin_question_included = True

        for _ in range(num_practical - 1):
            formula, _ = random.choice(practical_formulas)
            derivative = sp.diff(formula, x)
            wrong_derivatives = [sp.diff(f, x) for f, _ in random.sample(practical_formulas, 3)]
            all_answers = [derivative] + wrong_derivatives
            random.shuffle(all_answers)

            practical_question = {
                "question": f"Найдите производную функции: {formula}",
                "answers": [str(ans) for ans in all_answers],
                "correct": all_answers.index(derivative)
            }

            questions.append(practical_question)

        return questions