import streamlit as st
import datetime
import json
import os

# Настройки на страницата
st.set_page_config(page_title="Офис Паркинг", page_icon="🚗", layout="centered")

# Файл за съхранение на данните
DATA_FILE = "parking_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Списък с официалните празници в България за 2026 г.
def is_bulgarian_holiday(date):
    holidays_2026 = {
        datetime.date(2026, 1, 1),   # Нова година
        datetime.date(2026, 3, 3),   # Ден на Освобождението
        datetime.date(2026, 4, 10),  # Велики петък (Великден)
        datetime.date(2026, 4, 11),  # Велика събота
        datetime.date(2026, 4, 12),  # Великден
        datetime.date(2026, 4, 13),  # Великден - понеделник
        datetime.date(2026, 5, 1),   # Ден на труда
        datetime.date(2026, 5, 6),   # Гергьовден
        datetime.date(2026, 5, 24),  # Ден на светите братя Кирил и Методий
        datetime.date(2026, 5, 25),  # Почивен ден за 24 май
        datetime.date(2026, 9, 6),   # Съединението на България
        datetime.date(2026, 9, 7),   # Почивен ден за 6 септември
        datetime.date(2026, 9, 22),  # Ден на Независимостта
        datetime.date(2026, 12, 24), # Бъдни вечер
        datetime.date(2026, 12, 25), # Рождество Христово
        datetime.date(2026, 12, 26), # Рождество Христово
    }
    return date in holidays_2026

# Инициализация на данните
data = load_data()

# АВТОМАТИЧНА КОРЕКЦИЯ: Прехвърляне на старите резервации от "Утре" към днешната реална дата
today = datetime.date.today()
today_str = str(today)

if "Утре" in data and len(data["Утре"]) > 0:
    # Ако за днешната дата няма нищо, прехвърляме хората от стария ключ "Утре"
    if today_str not in data or len(data[today_str]) == 0:
        data[today_str] = data["Утре"]
    # Изтриваме стария ключ "Утре", за да не пречи повече
    del data["Утре"]
    save_data(data)

# Заглавие на приложението
st.title("🚗 Офис Паркинг Места")
st.markdown("Удобно и бързо запазване на паркоместа за екипа.")

# Генериране на 5 работни дни напред
days_options = []
days_mapping = {}

current_date = today
while len(days_options) < 5:
    if current_date.weekday() < 5 and not is_bulgarian_holiday(current_date):
        if current_date == today:
            label = f"Днес ({current_date.strftime('%d.%m')})"
        elif current_date == today + datetime.timedelta(days=1):
            label = f"Утре ({current_date.strftime('%d.%m')})"
        else:
            bg_days = ["Пон", "Втор", "Сряд", "Четв", "Пет", "Съб", "Нед"]
            day_name = bg_days[current_date.weekday()]
            label = f"{day_name} ({current_date.strftime('%d.%m')})"
            
        days_options.append(label)
        days_mapping[label] = str(current_date)
    
    current_date += datetime.timedelta(days=1)

selected_date = st.radio("Изберете ден:", days_options, horizontal=True)

# Ключ за базата данни според избрания ден
date_key = days_mapping[selected_date]

if date_key not in data:
    data[date_key] = []

reserved_players = data[date_key]
slots_taken = len(reserved_players)
max_slots = 5
slots_left = max_slots - slots_taken

# Визуализация на свободните места
st.subheader(f"Статус за избрания ден:")
if slots_left > 0:
    st.success(f"🔓 Свободни места: {slots_left} от {max_slots}")
else:
    st.error("🔴 ВСИЧКИ МЕСТА СА ЗАЕТИ!")

# Показване на графични "кутийки"
cols = st.columns(max_slots)
for i in range(max_slots):
    with cols[i]:
        if i < slots_taken:
            st.markdown(f"<div style='background-color:#ff4b4b; color:white; padding:10px; border-radius:5px; text-align:center; font-weight:bold;'>🚗<br>{reserved_players[i]}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background-color:#28a745; color:white; padding:10px; border-radius:5px; text-align:center; font-weight:bold;'>🟢<br>Свободно</div>", unsafe_allow_html=True)

st.markdown("---")

# ... (останалата част от формата си остава същата)
st.subheader("Управление на твоята reservation")

name = st.text_input("Въведи своето име (на кирилица):").strip()

if name:
    if name in reserved_players:
        st.warning(f"Ти ({name}) вече имаш запазено място за този ден.")
        if st.button("❌ Освободи моето място", type="secondary"):
            reserved_players.remove(name)
            data[date_key] = reserved_players
            save_data(data)
            st.rerun()
    else:
        if slots_left > 0:
            if st.button("✅ Запази място", type="primary"):
                reserved_players.append(name)
                data[date_key] = reserved_players
                save_data(data)
                st.rerun()
        else:
            st.info("Няма свободни места. Можеш да изчакаш някой колега да освободи своето.")
else:
    st.info("Моля, въведете името си горе, за да запазите или освободите място.")

if slots_taken > 0:
    st.markdown("### 📋 Списък на колегите с паркомясто:")
    for idx, player in enumerate(reserved_players, start=1):
        st.markdown(f"**{idx}. {player}**")
