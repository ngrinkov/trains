import streamlit as st
import json
from datetime import datetime
import pandas as pd
from pathlib import Path

# Настройка страницы
st.set_page_config(
    page_title="Дашборд ассистента CEO",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Путь к файлу данных
DATA_FILE = Path("dashboard_data.json")
NOTES_FILE = Path("department_notes.json")
ICONS_FILE = Path("department_icons.json")

# Инициализация данных
def load_data():
    """Загрузка данных из файла"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Начальные данные
        return {
            "Медиабаинг": [
                {
                    "title": "Упал ROI на Facebook на 40%",
                    "description": "Последние 3 дня показатели эффективности кампаний резко упали.",
                    "priority": "critical",
                    "status": "in_progress",
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "Креативы": [],
            "Аналитика": []
        }

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_notes():
    if NOTES_FILE.exists():
        with open(NOTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_notes(notes):
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

def load_icons():
    if ICONS_FILE.exists():
        with open(ICONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "Медиабаинг": "🎯",
        "Креативы": "🎨",
        "Аналитика": "📊",
        "Технический отдел": "⚙️",
        "Клоакинг": "🔒",
        "Финансы": "💵"
    }

def save_icons(icons):
    with open(ICONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(icons, f, ensure_ascii=False, indent=2)

# Инициализация session state
if 'data' not in st.session_state:
    st.session_state.data = load_data()
if 'notes' not in st.session_state:
    st.session_state.notes = load_notes()
if 'icons' not in st.session_state:
    st.session_state.icons = load_icons()
if 'active_department' not in st.session_state:
    st.session_state.active_department = None
if 'filter' not in st.session_state:
    st.session_state.filter = 'all'

# CSS стили
st.markdown("""
<style>
    .stApp { background-color: #0f172a; }
    .main-header { color: #ffffff; font-size: 32px; font-weight: 800; }
    .subtitle { color: #94a3b8; font-size: 15px; }
    .stat-card { background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; }
    .stat-value { font-size: 36px; font-weight: 800; color: #ffffff; }
    .stat-label { color: #94a3b8; font-size: 14px; }
    .dept-card { background: #1e293b; padding: 25px; border-radius: 15px; border: 1px solid #334155; margin-bottom: 20px; }
    .dept-title { font-size: 20px; font-weight: 700; color: #ffffff; }
    .section-header { background: #1e293b; padding: 12px 15px; border-radius: 8px; margin: 15px 0; font-weight: 600; color: #f1f5f9; }
</style>
""", unsafe_allow_html=True)

# Логика функций
def get_task_stats(tasks):
    total = len(tasks)
    critical = sum(1 for t in tasks if t['priority'] == 'critical' and t['status'] != 'completed')
    completed = sum(1 for t in tasks if t['status'] == 'completed')
    return total, critical, completed

def get_progress_percent(tasks):
    if not tasks: return 0
    completed = sum(1 for t in tasks if t['status'] == 'completed')
    return int((completed / len(tasks)) * 100)

def filter_tasks(tasks, filter_type):
    if filter_type == 'all': return tasks
    if filter_type == 'critical': return [t for t in tasks if t['priority'] == 'critical' and t['status'] != 'completed']
    if filter_type == 'normal': return [t for t in tasks if t['priority'] == 'normal' and t['status'] != 'completed']
    if filter_type == 'completed': return [t for t in tasks if t['status'] == 'completed']
    return tasks

# Боковая панель
with st.sidebar:
    st.markdown("### 📊 Arbitrage")
    if st.button("🏠 Дашборд", use_container_width=True):
        st.session_state.active_department = None
        st.rerun()
    
    st.markdown("#### Отделы")
    for dept in list(st.session_state.data.keys()):
        icon = st.session_state.icons.get(dept, "📁")
        if st.button(f"{icon} {dept}", key=f"dept_{dept}", use_container_width=True):
            st.session_state.active_department = dept
            st.rerun()

# Основной контент
if st.session_state.active_department:
    icon = st.session_state.icons.get(st.session_state.active_department, "📁")
    st.markdown(f"<div class='main-header'>{icon} {st.session_state.active_department}</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='main-header'>Дашборд ассистента CEO</div>", unsafe_allow_html=True)

# Кнопка создания
if st.button("➕ Новая задача"):
    st.session_state.show_add_modal = True

# Отображение задач (упрощенная логика для примера)
departments_to_show = {st.session_state.active_department: st.session_state.data[st.session_state.active_department]} if st.session_state.active_department else st.session_state.data

for dept, tasks in departments_to_show.items():
    st.markdown(f"<div class='dept-card'><div class='dept-title'>{dept}</div>", unsafe_allow_html=True)
    filtered = filter_tasks(tasks, st.session_state.filter)
    
    for idx, task in enumerate(filtered):
        with st.expander(f"{task['title']}"):
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            with col3:
                if st.button("✏️", key=f"edit_{dept}_{idx}"):
                    st.session_state.edit_task = (dept, idx)
                    st.rerun()
            with col4:
                if st.button("🗑️", key=f"del_{dept}_{idx}"):
                    st.session_state.data[dept].pop(idx)
                    save_data(st.session_state.data)
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Модальное окно добавления
if st.session_state.get('show_add_modal'):
    with st.form("add_task"):
        st.write("Новая задача")
        new_title = st.text_input("Заголовок")
        submitted = st.form_submit_button("Добавить")
        if submitted and new_title:
            # Логика добавления...
            st.session_state.show_add_modal = False
            st.rerun()
