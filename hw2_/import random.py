import numpy as np
import unittest

# Основная логика
def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)

def calculate_department_average(threat_scores):
    return np.mean(threat_scores) if len(threat_scores) > 0 else 0

def calculate_aggregated_threat(departments):
    total_threat = 0
    total_users = 0
    global_threat = 0  # Эта переменная будет использоваться для глобальной угрозы

    for department in departments:
        department_threat = np.sum(department['scores'])  # Суммируем угрозы пользователей
        num_users = len(department['scores'])  # Считаем количество пользователей

        # Проверяем, сколько пользователей в департаменте превысили уровень 55
        num_high_risk_users = sum(score > 55 for score in department['scores'])

        # Если хотя бы один пользователь превышает 55, но меньше половины
        if num_high_risk_users > 0 and num_high_risk_users < num_users / 2:
            max_threat = max(department['scores'])
            global_threat = max(global_threat, 55 + (max_threat - 70))  # Ставим угрозу на уровне 55 + (макс - 70)

        # Если больше половины пользователей превышают 55
        if num_high_risk_users >= num_users / 2:
            department_mean_threat = calculate_department_average(department['scores'])
            global_threat = max(global_threat, department_mean_threat)  # Ставим угрозу на уровне среднего департамента нарушителя



        # Добавляем угрозу департамента в общий подсчет
        total_threat += department_threat
        total_users += num_users

    # Возвращаем либо глобальную угрозу, либо среднюю угрозу
    return min(global_threat, 90) if global_threat > 0 else total_threat / total_users if total_users > 0 else 0

# Тесты
class TestAggregatedThreatScore(unittest.TestCase):

    def test_case_1_similar_scores(self):
        departments = [
            {'name': 'Engineering', 'scores': generate_random_data(30, 5, 50)},
            {'name': 'Marketing', 'scores': generate_random_data(30, 5, 50)},
            {'name': 'Finance', 'scores': generate_random_data(30, 5, 50)},
            {'name': 'HR', 'scores': generate_random_data(30, 5, 50)},
            {'name': 'Science', 'scores': generate_random_data(30, 5, 50)},
        ]
        aggregated_score = calculate_aggregated_threat(departments)
        print(f"Aggregated Score for Case 1 (similar scores): {aggregated_score}")
        self.assertAlmostEqual(aggregated_score, 30, delta=5)

    def test_case_2_high_vs_low_scores(self):
        departments = [
            {'name': 'Engineering', 'scores': generate_random_data(10, 5, 50)},
            {'name': 'Marketing', 'scores': generate_random_data(80, 5, 50)},  # Высокие угрозы
            {'name': 'Finance', 'scores': generate_random_data(10, 5, 50)},
            {'name': 'HR', 'scores': generate_random_data(10, 5, 50)},
            {'name': 'Science', 'scores': generate_random_data(10, 5, 50)},
        ]
        aggregated_score = calculate_aggregated_threat(departments)
        print(f"Aggregated Score for Case 2 (high vs low): {aggregated_score}")
        self.assertGreater(aggregated_score, 50)

    def test_case_3_high_individual_threat(self):
        departments = [
            {'name': 'Engineering', 'scores': generate_random_data(30, 5, 50)},
            {'name': 'Marketing', 'scores': generate_random_data(30, 5, 50)},
            {'name': 'Finance', 'scores': np.append(generate_random_data(30, 5, 49), [90])},  # Один пользователь с угрозой 90
            {'name': 'HR', 'scores': generate_random_data(30, 5, 50)},
            {'name': 'Science', 'scores': generate_random_data(30, 5, 50)},
        ]
        aggregated_score = calculate_aggregated_threat(departments)
        print(f"Aggregated Score for Case 3 (high individual threat): {aggregated_score}")
        self.assertGreater(aggregated_score, 55)

    def test_case_4_varied_user_counts(self):
        departments = [
            {'name': 'Engineering', 'scores': generate_random_data(30, 5, 200)},
            {'name': 'Marketing', 'scores': generate_random_data(30, 5, 50)},
            {'name': 'Finance', 'scores': generate_random_data(30, 5, 100)},
            {'name': 'HR', 'scores': generate_random_data(30, 5, 150)},
            {'name': 'Science', 'scores': generate_random_data(30, 5, 10)},
        ]
        aggregated_score = calculate_aggregated_threat(departments)
        print(f"Aggregated Score for Case 4 (varied user counts): {aggregated_score}")
        self.assertAlmostEqual(aggregated_score, 30, delta=5)


if __name__ == '__main__':
    unittest.main()
