import streamlit as st
import datetime
import json
import os

# Настройки на страницата
st.set_page_config(page_title="Офис Паркинг", page_icon="🚗", layout="centered")

# Файл за съхранение на данните (локална псевдо-база данни)
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

# Инициализация на данните
data = load_data()

# Заглавие на приложението
st.title("🚗 Офис Паркинг Места")
st.markdown("Удобно и бързо запазване на паркоместа за екипа.")

# Избор на дата (ограничена до днес и утре за лесна ротация)
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
selected_date = st.radio("Изберете ден:", [f"Днес ({today.strftime('%d.%m')})", f"Утре ({tomorrow.strftime('%d.%m')})"], horizontal=True)

# Ключ за базата данни според избрания ден
date_key = str(today) if "Днес" in selected_date else str(tomorrow)

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

# Показване на графични "кутийки" за заетите места
cols = st.columns(max_slots)
for i in range(max_slots):
    with cols[i]:
        if i < slots_taken:
            st.markdown(f"<div style='background-color:#ff4b4b; color:white; padding:10px; border-radius:5px; text-align:center; font-weight:bold;'>🚗<br>{reserved_players[i]}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background-color:#28a745; color:white; padding:10px; border-radius:5px; text-align:center; font-weight:bold;'>🟢<br>Свободно</div>", unsafe_allow_html=True)

st.markdown("---")

# Форма за запазване / освобождаване
st.subheader("Управление на твоята резервация")

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

# Списък на записаните колеги за деня
if slots_taken > 0:
    st.markdown("### 📋 Списък на колегите с паркомясто:")
    for idx, player in enumerate(reserved_players, start=1):
        st.markdown(f"**{idx}. {player}**")
