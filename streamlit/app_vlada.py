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
                    "description": "Последние 3 дня показатели эффективности кампаний резко упали. Требуется срочный анализ и корректировка стратегии.",
                    "priority": "critical",
                    "status": "in_progress",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "title": "Проверить новые аккаунты TikTok",
                    "description": "5 новых акков требуют настройки и запуска тестовых кампаний.",
                    "priority": "normal",
                    "status": "not_started",
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "Креативы": [
                {
                    "title": "Создать 10 новых креативов для nutra-оффера",
                    "description": "Нужны вариации под разные ГЕО: EN, ES, DE. Дедлайн - конец дня.",
                    "priority": "critical",
                    "status": "in_progress",
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "Аналитика": [
                {
                    "title": "Отчёт по эффективности источников за неделю",
                    "description": "Подготовить детальный отчёт для CEO с рекомендациями по масштабированию.",
                    "priority": "normal",
                    "status": "in_progress",
                    "timestamp": datetime.now().isoformat()
                }
            ]
        }

def save_data(data):
    """Сохранение данных в файл"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_notes():
    """Загрузка заметок отделов"""
    if NOTES_FILE.exists():
        with open(NOTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_notes(notes):
    """Сохранение заметок"""
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

def load_icons():
    """Загрузка иконок отделов"""
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
    """Сохранение иконок"""
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
    .stApp {
        background-color: #0f172a;
    }
    .main-header {
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #94a3b8;
        font-size: 15px;
        margin-bottom: 30px;
    }
    .stat-card {
        background: #1e293b;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    .stat-value {
        font-size: 36px;
        font-weight: 800;
        color: #ffffff;
    }
    .stat-label {
        color: #94a3b8;
        font-size: 14px;
    }
    .dept-card {
        background: #1e293b;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }
    .dept-title {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 15px;
    }
    .task-item {
        background: #0f172a;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 12px;
        border-left: 4px solid;
    }
    .task-critical {
        border-left-color: #ef4444;
    }
    .task-normal {
        border-left-color: #10b981;
    }
    .task-title {
        font-weight: 600;
        color: #f1f5f9;
        font-size: 15px;
    }
    .task-description {
        color: #94a3b8;
        font-size: 14px;
        margin-top: 8px;
    }
    .progress-bar {
        height: 12px;
        background: #1e293b;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #334155;
    }
    .section-header {
        background: #1e293b;
        padding: 12px 15px;
        border-radius: 8px;
        margin: 15px 0;
        font-weight: 600;
        color: #f1f5f9;
    }
</style>
""", unsafe_allow_html=True)

# Функции для работы с задачами
def get_task_stats(tasks):
    """Получить статистику по задачам"""
    total = len(tasks)
    critical = sum(1 for t in tasks if t['priority'] == 'critical' and t['status'] != 'completed')
    completed = sum(1 for t in tasks if t['status'] == 'completed')
    return total, critical, completed

def get_progress_percent(tasks):
    """Рассчитать процент выполнения"""
    if not tasks:
        return 0
    completed = sum(1 for t in tasks if t['status'] == 'completed')
    return int((completed / len(tasks)) * 100)

def filter_tasks(tasks, filter_type):
    """Фильтрация задач"""
    if filter_type == 'all':
        return tasks
    elif filter_type == 'critical':
        return [t for t in tasks if t['priority'] == 'critical' and t['status'] != 'completed']
    elif filter_type == 'normal':
        return [t for t in tasks if t['priority'] == 'normal' and t['status'] != 'completed']
    elif filter_type == 'completed':
        return [t for t in tasks if t['status'] == 'completed']
    return tasks

# Боковая панель
with st.sidebar:
    st.markdown("### 📊 Arbitrage")
    st.markdown("---")
    
    st.markdown("#### Меню")
    if st.button("🏠 Дашборд", use_container_width=True):
        st.session_state.active_department = None
        st.rerun()
    
    st.markdown("#### Отделы")
    for dept in st.session_state.data.keys():
        icon = st.session_state.icons.get(dept, "📁")
        if st.button(f"{icon} {dept}", key=f"dept_{dept}", use_container_width=True):
            st.session_state.active_department = dept
            st.rerun()
    
    st.markdown("---")
    
    # Управление отделами
    with st.expander("⚙️ Управление отделами"):
        new_dept_name = st.text_input("Название отдела")
        new_dept_icon = st.text_input("Иконка (emoji)", value="📁")
        if st.button("➕ Добавить отдел"):
            if new_dept_name and new_dept_name not in st.session_state.data:
                st.session_state.data[new_dept_name] = []
                st.session_state.icons[new_dept_name] = new_dept_icon
                save_data(st.session_state.data)
                save_icons(st.session_state.icons)
                st.success(f"Отдел '{new_dept_name}' добавлен!")
                st.rerun()
    
    # Экспорт/Импорт
    st.markdown("---")
    st.markdown("#### 📥 Экспорт/Импорт")
    
    # Экспорт
    export_data = {
        "version": "1.0",
        "exportDate": datetime.now().isoformat(),
        "dashboardData": st.session_state.data,
        "departmentIcons": st.session_state.icons,
        "departmentNotes": st.session_state.notes
    }
    st.download_button(
        label="📥 Экспортировать данные",
        data=json.dumps(export_data, ensure_ascii=False, indent=2),
        file_name=f"dashboard-backup-{datetime.now().strftime('%Y-%m-%d')}.json",
        mime="application/json",
        use_container_width=True
    )
    
    # Импорт
    uploaded_file = st.file_uploader("📤 Импортировать данные", type=['json'])
    if uploaded_file is not None:
        import_data = json.load(uploaded_file)
        if st.button("✅ Подтвердить импорт", use_container_width=True):
            st.session_state.data = import_data['dashboardData']
            st.session_state.icons = import_data['departmentIcons']
            st.session_state.notes = import_data.get('departmentNotes', {})
            save_data(st.session_state.data)
            save_icons(st.session_state.icons)
            save_notes(st.session_state.notes)
            st.success("Данные импортированы!")
            st.rerun()

# Основной контент
if st.session_state.active_department:
    icon = st.session_state.icons.get(st.session_state.active_department, "📁")
    st.markdown(f"<div class='main-header'>{icon} {st.session_state.active_department}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>Задачи отдела {st.session_state.active_department}</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='main-header'>Дашборд ассистента CEO</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Обзор задач и проблем арбитражной команды</div>", unsafe_allow_html=True)

# Кнопки действий
col1, col2, col3 = st.columns([6, 1, 1])
with col2:
    if st.button("➕ Новая задача", use_container_width=True):
        st.session_state.show_add_modal = True

# Статистика
departments_to_show = {st.session_state.active_department: st.session_state.data[st.session_state.active_department]} if st.session_state.active_department else st.session_state.data

total_tasks = 0
critical_tasks = 0
completed_tasks = 0

for dept, tasks in departments_to_show.items():
    total_tasks += len(tasks)
    critical_tasks += sum(1 for t in tasks if t['priority'] == 'critical' and t['status'] != 'completed')
    completed_tasks += sum(1 for t in tasks if t['status'] == 'completed')

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class='stat-card'>
        <div class='stat-value'>{total_tasks}</div>
        <div class='stat-label'>Всего задач</div>
    </div>
    """, unsafe_allow_html=True)

Влада, [28.02.2026 23:38]
with col2:
    st.markdown(f"""
    <div class='stat-card'>
        <div class='stat-value'>{critical_tasks}</div>
        <div class='stat-label'>Критические</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='stat-card'>
        <div class='stat-value'>{completed_tasks}</div>
        <div class='stat-label'>Завершено</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Фильтры
st.markdown("### Фильтры")
filter_cols = st.columns(4)
with filter_cols[0]:
    if st.button("Все задачи", use_container_width=True, type="primary" if st.session_state.filter == 'all' else "secondary"):
        st.session_state.filter = 'all'
        st.rerun()
with filter_cols[1]:
    if st.button("🔴 Критические", use_container_width=True, type="primary" if st.session_state.filter == 'critical' else "secondary"):
        st.session_state.filter = 'critical'
        st.rerun()
with filter_cols[2]:
    if st.button("🟢 Обычные", use_container_width=True, type="primary" if st.session_state.filter == 'normal' else "secondary"):
        st.session_state.filter = 'normal'
        st.rerun()
with filter_cols[3]:
    if st.button("✅ Завершённые", use_container_width=True, type="primary" if st.session_state.filter == 'completed' else "secondary"):
        st.session_state.filter = 'completed'
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Отображение отделов
for dept, tasks in departments_to_show.items():
    icon = st.session_state.icons.get(dept, "📁")
    
    with st.container():
        st.markdown(f"<div class='dept-card'>", unsafe_allow_html=True)
        
        # Заголовок отдела
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"<div class='dept-title'>{icon} {dept}</div>", unsafe_allow_html=True)
        with col2:
            active_count = len([t for t in tasks if t['status'] != 'completed'])
            st.markdown(f"**{active_count} активных**")
        
        # Статистика отдела
        total, critical, completed = get_task_stats(tasks)
        st.markdown(f"📋 {total} всего | ✅ {completed} выполнено")
        
        # Заметки и проблемы
        st.markdown("---")
        st.markdown("**📝 Заметки и проблемы**")
        notes_key = f"notes_{dept}"
        current_notes = st.session_state.notes.get(dept, "")
        new_notes = st.text_area(
            "Нажмите для добавления заметок...",
            value=current_notes,
            key=notes_key,
            height=100,
            label_visibility="collapsed"
        )
        if new_notes != current_notes:
            st.session_state.notes[dept] = new_notes
            save_notes(st.session_state.notes)
        
        # Прогресс выполнения
        st.markdown("---")
        progress = get_progress_percent(tasks)
        st.markdown(f"**📊 Прогресс выполнения: {progress}%**")
        st.progress(progress / 100)
        
        # Задачи
        st.markdown("---")
        filtered_tasks = filter_tasks(tasks, st.session_state.filter)
        
        # Разделение на активные и завершённые
        active_tasks = [t for t in filtered_tasks if t['status'] != 'completed']
        completed_tasks_list = [t for t in filtered_tasks if t['status'] == 'completed']
        
        # Активные задачи
        if active_tasks:
            st.markdown("<div class='section-header'>🔄 В работе</div>", unsafe_allow_html=True)
            for idx, task in enumerate(active_tasks):
                original_idx = tasks.index(task)
                
                with st.expander(f"{'🔴' if task['priority'] == 'critical' else '🟢'} {task['title']}", expanded=False):
                    st.markdown(f"**Описание:** {task['description']}")
                    
                    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                    
                    with col1:
                        new_status = st.selectbox(
                            "Статус",
                            ["not_started", "in_progress", "completed"],
                            index=["not_started", "in_progress", "completed"].index(task['status']),
                            format_func=lambda x: {"not_started": "⚪ Не взята", "in_progress": "🔵 В работе", "completed": "✅ Выполнена"}[x],
                            key=f"status_{dept}_{original_idx}"
                        )
                        if new_status != task['status']:
                            st.session_state.data[dept][original_idx]['status'] = new_status
                            save_data(st.session_state.data)
                            st.rerun()
                    
                    with col2:
                        new_priority = st.selectbox(
                            "Приоритет",
                            ["normal", "critical"],
                            index=["normal", "critical"].index(task['priority']),
                            format_func=lambda x: {"normal": "🟢 Обычный", "critical": "🔴 Критический"}[x],
                            key=f"priority_{dept}_{original_idx}"
                        )
                        if new_priority != task['priority']:
                            st.session_state.data[dept][original_idx]['priority'] = new_priority
                            save_data(st.session_state.data)
                            st.rerun()
                    
                    with col3:
                        if st.button("✏️", key=f"edit_{dept}_{original_idx}"):

st.session_state.edit_task = (dept, original_idx)
                            st.rerun()
                    
                    with col4:
                        if st.button("🗑️", key=f"delete_{dept}_{original_idx}"):
                            st.session_state.data[dept].pop(original_idx)
                            save_data(st.session_state.data)
                            st.success("Задача удалена!")
                            st.rerun()
        
        # Завершённые задачи
        if completed_tasks_list:
            st.markdown("<div class='section-header'>✅ Завершено</div>", unsafe_allow_html=True)
            with st.expander(f"Показать завершённые ({len(completed_tasks_list)})", expanded=False):
                for task in completed_tasks_list:
                    st.markdown(f"- ~~{task['title']}~~")
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

# Модальное окно добавления задачи
if 'show_add_modal' in st.session_state and st.session_state.show_add_modal:
    with st.form("add_task_form"):
        st.markdown("### ➕ Новая задача")
        
        dept = st.selectbox("Отдел", list(st.session_state.data.keys()))
        title = st.text_input("Название задачи")
        description = st.text_area("Описание")
        priority = st.selectbox("Приоритет", ["normal", "critical"], format_func=lambda x: {"normal": "🟢 Обычный", "critical": "🔴 Критический"}[x])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Добавить", use_container_width=True):
                if title:
                    st.session_state.data[dept].append({
                        "title": title,
                        "description": description,
                        "priority": priority,
                        "status": "not_started",
                        "timestamp": datetime.now().isoformat()
                    })
                    save_data(st.session_state.data)
                    st.session_state.show_add_modal = False
                    st.success("Задача добавлена!")
                    st.rerun()
        with col2:
            if st.form_submit_button("Отмена", use_container_width=True):
                st.session_state.show_add_modal = False
                st.rerun()

# Модальное окно редактирования задачи
if 'edit_task' in st.session_state:
    dept, idx = st.session_state.edit_task
    task = st.session_state.data[dept][idx]
    
    with st.form("edit_task_form"):
        st.markdown("### ✏️ Редактировать задачу")
        
        title = st.text_input("Название задачи", value=task['title'])
        description = st.text_area("Описание", value=task['description'])
        priority = st.selectbox(
            "Приоритет",
            ["normal", "critical"],
            index=["normal", "critical"].index(task['priority']),
            format_func=lambda x: {"normal": "🟢 Обычный", "critical": "🔴 Критический"}[x]
        )
        status = st.selectbox(
            "Статус",
            ["not_started", "in_progress", "completed"],
            index=["not_started", "in_progress", "completed"].index(task['status']),
            format_func=lambda x: {"not_started": "⚪ Не взята", "in_progress": "🔵 В работе", "completed": "✅ Выполнена"}[x]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Сохранить", use_container_width=True):
                st.session_state.data[dept][idx].update({
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "status": status
                })
                save_data(st.session_state.data)
                del st.session_state.edit_task
                st.success("Задача обновлена!")
                st.rerun()
        with col2:
            if st.form_submit_button("Отмена", use_container_width=True):
                del st.session_state.edit_task
                st.rerun()
