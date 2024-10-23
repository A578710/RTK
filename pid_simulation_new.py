import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import streamlit as st

# Функція для створення ПІД-регулятора та системи з урахуванням навантаження
def simulate_pid(Kp, Ki, Kd, system, load_factor):
    # Передавальна функція ПІД-регулятора
    pid = ctrl.TransferFunction([Kd, Kp, Ki], [1, 0])

    # Вибір передавальної функції для системи залежно від сценарію
    if system == "Двигун":
        # Навантаження впливає на коефіцієнти передачі
        plant = ctrl.TransferFunction([1], [1, 3 + load_factor, 2 + 0.5 * load_factor])
    elif system == "Рівень води в резервуарі":
        plant = ctrl.TransferFunction([1], [1, 2, 1])
    elif system == "Температура в інкубаторі":
        plant = ctrl.TransferFunction([1], [1, 1.5, 1])
    elif system == "Клімат-контроль у кімнаті":
        # Навантаження моделює збурення в системі, що ускладнює підтримку стабільної роботи
        plant = ctrl.TransferFunction([1], [1, 2.5 + 0.3 * load_factor, 2])
    elif system == "Стабілізація дрона":
        # Додаткове навантаження збільшує інерційність системи
        plant = ctrl.TransferFunction([1], [1, 1 + load_factor, 0.5 + 0.2 * load_factor])

    # Замкнута система зворотного зв'язку
    closed_loop_system = ctrl.feedback(pid * plant, 1)

    # Моделювання системи
    time = np.linspace(0, 20, 1000)  # Час моделювання від 0 до 20 секунд
    t, y = ctrl.step_response(closed_loop_system, time)

    # Побудова графіку реакції системи
    fig, ax = plt.subplots()
    ax.plot(t, y)
    ax.set_title(f'Реакція системи: {system} при Kp={Kp}, Ki={Ki}, Kd={Kd} (Навантаження: {load_factor})')
    ax.set_xlabel('Час (секунди)')
    ax.set_ylabel('Вихід (реальні величини)')
    ax.grid(True)
    return fig

# Streamlit UI
st.title("ПІД-регулятор Симуляція з Емпіричним Методом та Навантаженням")
st.write("Виберіть завдання, налаштуйте параметри ПІД-регулятора і навантаження, щоб спостерігати за реакцією системи.")

# Список доступних сценаріїв (відповідно до завдань)
scenarios = [
    "Рівень води в резервуарі",
    "Температура в інкубаторі",
    "Двигун",
    "Клімат-контроль у кімнаті",
    "Стабілізація дрона"
]

# Вибір завдання
selected_scenario = st.selectbox("Виберіть сценарій", scenarios)

# Задаємо початкові значення параметрів залежно від сценарію
if selected_scenario == "Рівень води в резервуарі":
    default_Kp, default_Ki, default_Kd = 2.0, 0.5, 0.1
    load_control = False
elif selected_scenario == "Температура в інкубаторі":
    default_Kp, default_Ki, default_Kd = 5.0, 1.5, 0.2
    load_control = False
elif selected_scenario == "Двигун":
    default_Kp, default_Ki, default_Kd = 8.0, 2.0, 0.5
    load_control = True
elif selected_scenario == "Клімат-контроль у кімнаті":
    default_Kp, default_Ki, default_Kd = 3.0, 0.8, 0.3
    load_control = True
elif selected_scenario == "Стабілізація дрона":
    default_Kp, default_Ki, default_Kd = 10.0, 3.0, 1.0
    load_control = True

# Контролери для введення значень параметрів
Kp = st.number_input("Пропорційний коефіцієнт (Kp)", min_value=0.0, max_value=100.0, value=default_Kp, step=0.1)
Ki = st.number_input("Інтегральний коефіцієнт (Ki)", min_value=0.0, max_value=100.0, value=default_Ki, step=0.1)
Kd = st.number_input("Диференційний коефіцієнт (Kd)", min_value=0.0, max_value=100.0, value=default_Kd, step=0.1)

# Додатковий контролер для навантаження, якщо завдання передбачає зміну навантаження
if load_control:
    load_factor = st.slider("Навантаження (0 - без навантаження, 10 - високе навантаження)", 0, 10, 0)
else:
    load_factor = 0

# Запуск симуляції та виведення графіка
fig = simulate_pid(Kp, Ki, Kd, selected_scenario, load_factor)
st.pyplot(fig)

# Опис завдань для довідки
if selected_scenario == "Рівень води в резервуарі":
    st.info("Завдання: Підтримати рівень води на встановленому рівні, мінімізуючи коливання.")
elif selected_scenario == "Температура в інкубаторі":
    st.info("Завдання: Стабілізувати температуру в інкубаторі з точністю ±1°C.")
elif selected_scenario == "Двигун":
    st.info("Завдання: Контролювати швидкість двигуна для забезпечення швидкої та стабільної реакції на зміну навантаження.")
elif selected_scenario == "Клімат-контроль у кімнаті":
    st.info("Завдання: Підтримувати стабільну вологість у кімнаті, враховуючи збурення від зовнішніх факторів.")
elif selected_scenario == "Стабілізація дрона":
    st.info("Завдання: Стабілізувати положення дрона на заданій висоті, з урахуванням поривів вітру.")
