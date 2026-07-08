import streamlit as st
import datetime
import json
import os

# 1. Луксозни настройки на страницата с тъмна/модерна тема
st.set_page_config(
    page_title="Сердика Паркинг", 
    page_icon="🏎️", 
    layout="centered"
)

# Красив персонализиран CSS за луксозен дизайн и анимации
st.markdown("""
    <style>
    /* Премахване на стандартните полета за по-изчистен вид */
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    
    /* Стил за заглавието */
    .main-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 800;
        background: linear-gradient(45deg, #ff4b4b, #ff8585);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        text-align: center;
        color: #a3a8b4;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Луксозни картички за паркоместата */
    .parking-card {
        border-radius: 12px;
        padding: 20px 10px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 15px;
    }
    .parking-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    .card-free {
        background: linear-gradient(135deg, #28a745, #1e7e34);
        color: white;
        border: 1px solid #34ce57;
    }
    .card-taken {
        background: linear-gradient(135deg, #dc3545, #bd2130);
        color: white;
        border: 1px solid #e4606d;
    }
    
    /* Стилизиране на списъка с колеги */
    .user-badge {
        background-color: #1e222b;
        padding: 8px 12px;
        border-radius: 8px;
        border-left: 4px solid #ff4b4b;
        margin-bottom: 6px;
    }
    </style>
""", unsafe_allow_html=True)

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

def is_bulgarian_holiday(date):
    holidays_2026 = {
        datetime.date(2026, 1, 1), datetime.date(2026, 3, 3), datetime.date(2026, 4, 10),
        datetime.date(2026, 4, 11), datetime.date(2026, 4, 12), datetime.date(2026, 4, 13),
        datetime.date(2026, 5, 1), datetime.date(2026, 5, 6), datetime.date(2026, 5, 24),
        datetime.date(2026, 5, 25), datetime.date(2026, 9, 6), datetime.date(2026, 9, 7),
        datetime.date(2026, 9, 22), datetime.date(2026, 12, 24), datetime.date(2026, 12, 25),
        datetime.date(2026, 12, 26),
    }
    return date in holidays_2026

data = load_data()
today = datetime.date.today()

# Модерно заглавие
st.markdown("<h1 class='main-title'>🚗 SERDIKA PARKING</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Премиум система за резервация на споделени паркоместа</p>", unsafe_allow_html=True)

# Генериране на 5 работни дни
days_options = []
days_mapping = {}
current_date = today

while len(days_options) < 5:
    if current_date.weekday() < 5 and not is_bulgarian_holiday(current_date):
        if current_date == today:
            label = f"📅 Днес ({current_date.strftime('%d.%m')})"
        elif current_date == today + datetime.timedelta(days=1):
            label = f"🌅 Утре ({current_date.strftime('%d.%m')})"
        else:
            bg_days = ["Пон", "Втор", "Сряд", "Четв", "Пет", "Съб", "Нед"]
            day_name = bg_days[current_date.weekday()]
            label = f"{day_name} ({current_date.strftime('%d.%m')})"
            
        days_options.append(label)
        days_mapping[label] = str(current_date)
    current_date += datetime.timedelta(days=1)

# Интерактивен селектор за ден с по-изчистен вид
selected_date = st.radio("Изберете работен ден:", days_options, horizontal=True, label_visibility="collapsed")
date_key = days_mapping[selected_date]

if date_key not in data:
    data[date_key] = []

reserved_players = data[date_key]
slots_taken = len(reserved_players)
max_slots = 5
slots_left = max_slots - slots_taken

st.markdown("---")

# 2. Интерактивен Прогрес бар за заетост
occupancy_percentage = (slots_taken / max_slots)
st.markdown(f"**Заетост на паркинга:** {slots_taken} от {max_slots} места")
st.progress(occupancy_percentage)

# 3. Визуализация на луксозните картички
cols = st.columns(max_slots)
for i in range(max_slots):
    with cols[i]:
        if i < slots_taken:
            st.markdown(f"""
                <div class='parking-card card-taken'>
                    <span style='font-size: 1.5rem;'>🚘</span><br>
                    <span style='font-size: 0.9rem; display:block; margin-top:5px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;'>{reserved_players[i]}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class='parking-card card-free'>
                    <span style='font-size: 1.5rem;'>🟢</span><br>
                    <span style='font-size: 0.9rem; display:block; margin-top:5px;'>Свободно</span>
                </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# Форма за управление
st.subheader("🔒 Управление на резервацията")
name = st.text_input("Въведете вашето име (на кирилица):", placeholder="Напр. Иван Иванов").strip()

if name:
    if name in reserved_players:
        st.warning(f"Вие ({name}) вече имате запазено място за този ден.")
        if st.button("❌ Освободи моето място", use_container_width=True):
            reserved_players.remove(name)
            data[date_key] = reserved_players
            save_data(data)
            st.rerun()
    else:
        if slots_left > 0:
            if st.button("✨ Запази премиум място", type="primary", use_container_width=True):
                reserved_players.append(name)
                data[date_key] = reserved_players
                save_data(data)
                st.rerun()
        else:
            st.error("Всички места за този ден са изчерпани!")
else:
    st.info("Въведете името си по-горе, за да отключите бутоните за запазване.")

# Списък под формата на модерни баджове
if slots_taken > 0:
    st.markdown("### 📋 Екип с резервация за деня:")
    for idx, player in enumerate(reserved_players, start=1):
        st.markdown(f"<div class='user-badge'><b>{idx}.</b> {player}</div>", unsafe_allow_html=True)
