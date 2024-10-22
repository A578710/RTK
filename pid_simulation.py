import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import streamlit as st

# Функція для створення ПІД-регулятора та системи
def simulate_pid(Kp, Ki, Kd, system):
    # Передавальна функція ПІД-регулятора
    pid = ctrl.TransferFunction([Kd, Kp, Ki], [1, 0])

    # Вибір передавальної функції для системи залежно від сценарію
    if system == "Двигун":
        plant = ctrl.TransferFunction([1], [1, 3, 2])
    elif system == "Рівень води в резервуарі":
        plant = ctrl.TransferFunction([1], [1, 2, 1])
    elif system == "Температура в інкубаторі":
        plant = ctrl.TransferFunction([1], [1, 1.5, 1])
    elif system == "Клімат-контроль у кімнаті":
        plant = ctrl.TransferFunction([1], [1, 2.5, 2])
    elif system == "Стабілізація дрона":
        plant = ctrl.TransferFunction([1], [1, 1, 0.5])

    # Замкнута система зворотного зв'язку
    closed_loop_system = ctrl.feedback(pid * plant, 1)

    # Моделювання системи
    time = np.linspace(0, 20, 1000)  # Час моделювання від 0 до 20 секунд
    t, y = ctrl.step_response(closed_loop_system, time)

    # Побудова графіку реакції системи
    fig, ax = plt.subplots()
    ax.plot(t, y)
    ax.set_title(f'Реакція системи: {system} при Kp={Kp}, Ki={Ki}, Kd={Kd}')
    ax.set_xlabel('Час (секунди)')
    ax.set_ylabel('Вихід')
    ax.grid(True)
    return fig

# Streamlit UI
st.title("ПІД-регулятор Симуляція з Емпіричним Методом")
st.write("Виберіть завдання та налаштуйте параметри ПІД-регулятора, щоб спостерігати за реакцією системи.")

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
elif selected_scenario == "Температура в інкубаторі":
    default_Kp, default_Ki, default_Kd = 5.0, 1.5, 0.2
elif selected_scenario == "Двигун":
    default_Kp, default_Ki, default_Kd = 8.0, 2.0, 0.5
elif selected_scenario == "Клімат-контроль у кімнаті":
    default_Kp, default_Ki, default_Kd = 3.0, 0.8, 0.3
elif selected_scenario == "Стабілізація дрона":
    default_Kp, default_Ki, default_Kd = 10.0, 3.0, 1.0

# Контролери для введення значень параметрів
Kp = st.number_input("Пропорційний коефіцієнт (Kp)", min_value=0.0, max_value=100.0, value=default_Kp, step=0.1)
Ki = st.number_input("Інтегральний коефіцієнт (Ki)", min_value=0.0, max_value=100.0, value=default_Ki, step=0.1)
Kd = st.number_input("Диференційний коефіцієнт (Kd)", min_value=0.0, max_value=100.0, value=default_Kd, step=0.1)

# Запуск симуляції та виведення графіка
fig = simulate_pid(Kp, Ki, Kd, selected_scenario)
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
