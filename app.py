import random
import sqlite3
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="MindAge",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

DB_NAME = "mindage.db"


# =========================================================
# TRANSLATIONS
# =========================================================

TEXT = {
    "English": {
        "tagline": "Cognitive Engagement & Progress Tracking",
        "intro": "Interactive cognitive activities with personal progress tracking.",
        "notice": "Educational prototype only. MindAge is not a medical device and does not diagnose or predict Alzheimer's disease.",
        "language": "Language",
        "participant": "Participant ID",
        "navigation": "Navigation",
        "memory": "Memory Training",
        "attention": "Attention Training",
        "pattern": "Pattern Recognition",
        "history": "Progress History",
        "theme": "Appearance",
        "light": "Light",
        "dark": "Dark",
        "difficulty": "Choose difficulty",
        "easy": "Easy",
        "medium": "Medium",
        "hard": "Hard",
        "recommended": "Recommended level",
        "recommendation_note": "Based on the last three activities",
        "not_enough": "Complete three activities to receive a recommendation.",
        "new_round": "Start a New Round",
        "memory_hint": "Memorize the words and then recall them.",
        "hide_words": "Hide the words",
        "recall": "Enter the words you remember, separated by commas.",
        "check": "Check answers",
        "attention_hint": "Select every symbol that matches the target.",
        "target": "Target symbol",
        "pattern_hint": "Choose the next number in each sequence.",
        "question": "Question",
        "submit": "Submit",
        "score": "Score",
        "accuracy": "Accuracy",
        "saved": "Your result has been saved.",
        "total": "Completed activities",
        "average": "Average accuracy",
        "latest": "Latest accuracy",
        "no_history": "No results yet. Complete an activity to see your progress.",
        "activity": "Activity",
        "level": "Difficulty",
        "date": "Date",
        "progress": "Progress over time",
        "footer": "MindAge is a student-built educational prototype. Results are not clinical assessments.",
        "words": [
            "garden", "window", "river", "pencil",
            "cloud", "orange", "bridge", "music",
            "flower", "book", "mountain", "chair",
        ],
    },

    "Русский": {
        "tagline": "Когнитивные упражнения и отслеживание прогресса",
        "intro": "Интерактивные когнитивные упражнения с отслеживанием результатов.",
        "notice": "Образовательный прототип. MindAge не является медицинским устройством и не диагностирует и не прогнозирует болезнь Альцгеймера.",
        "language": "Язык",
        "participant": "ID участника",
        "navigation": "Навигация",
        "memory": "Тренировка памяти",
        "attention": "Тренировка внимания",
        "pattern": "Распознавание закономерностей",
        "history": "История прогресса",
        "theme": "Тема оформления",
        "light": "Светлая",
        "dark": "Тёмная",
        "difficulty": "Выбери сложность",
        "easy": "Лёгкий",
        "medium": "Средний",
        "hard": "Сложный",
        "recommended": "Рекомендуемый уровень",
        "recommendation_note": "На основе последних трёх упражнений",
        "not_enough": "Выполни три упражнения, чтобы получить рекомендацию.",
        "new_round": "Начать новый раунд",
        "memory_hint": "Запомни слова, а затем попробуй их воспроизвести.",
        "hide_words": "Скрыть слова",
        "recall": "Введи слова, которые запомнил(а), через запятую.",
        "check": "Проверить ответы",
        "attention_hint": "Выбери все символы, которые совпадают с целевым.",
        "target": "Целевой символ",
        "pattern_hint": "Выбери следующее число в каждой последовательности.",
        "question": "Вопрос",
        "submit": "Отправить",
        "score": "Результат",
        "accuracy": "Точность",
        "saved": "Результат сохранён.",
        "total": "Выполнено упражнений",
        "average": "Средняя точность",
        "latest": "Последняя точность",
        "no_history": "Пока нет результатов. Выполни упражнение, чтобы увидеть прогресс.",
        "activity": "Упражнение",
        "level": "Сложность",
        "date": "Дата",
        "progress": "Прогресс по упражнениям",
        "footer": "MindAge — учебный прототип. Результаты не являются клинической оценкой.",
        "words": [
            "сад", "окно", "река", "карандаш",
            "облако", "апельсин", "мост", "музыка",
            "цветок", "книга", "гора", "стул",
        ],
    },

    "Azərbaycan dili": {
        "tagline": "Koqnitiv tapşırıqlar və irəliləyişin izlənməsi",
        "intro": "İnteraktiv koqnitiv tapşırıqlar və nəticələrin izlənməsi.",
        "notice": "Yalnız təhsil məqsədlidir. MindAge tibbi cihaz deyil və Alzheimer xəstəliyini diaqnoz etmir və ya proqnozlaşdırmır.",
        "language": "Dil",
        "participant": "İştirakçı ID-si",
        "navigation": "Naviqasiya",
        "memory": "Yaddaş məşqi",
        "attention": "Diqqət məşqi",
        "pattern": "Qanunauyğunluqlar",
        "history": "İrəliləyiş tarixçəsi",
        "theme": "Görünüş",
        "light": "Açıq",
        "dark": "Tünd",
        "difficulty": "Çətinliyi seç",
        "easy": "Asan",
        "medium": "Orta",
        "hard": "Çətin",
        "recommended": "Tövsiyə olunan səviyyə",
        "recommendation_note": "Son üç tapşırığın nəticələrinə əsasən",
        "not_enough": "Tövsiyə almaq üçün üç tapşırıq tamamla.",
        "new_round": "Yeni raund başlat",
        "memory_hint": "Sözləri yadda saxla və sonra xatırlamağa çalış.",
        "hide_words": "Sözləri gizlət",
        "recall": "Yadında qalan sözləri vergüllə ayıraraq yaz.",
        "check": "Cavabları yoxla",
        "attention_hint": "Hədəf simvola uyğun olan bütün simvolları seç.",
        "target": "Hədəf simvol",
        "pattern_hint": "Ardıcıllıqda növbəti rəqəmi seç.",
        "question": "Sual",
        "submit": "Göndər",
        "score": "Nəticə",
        "accuracy": "Dəqiqlik",
        "saved": "Nəticə yadda saxlanıldı.",
        "total": "Tamamlanmış tapşırıqlar",
        "average": "Orta dəqiqlik",
        "latest": "Son dəqiqlik",
        "no_history": "Hələ nəticə yoxdur.",
        "activity": "Tapşırıq",
        "level": "Çətinlik",
        "date": "Tarix",
        "progress": "İrəliləyiş",
        "footer": "MindAge təhsil prototipidir. Nəticələr klinik qiymətləndirmə deyil.",
        "words": [
            "bağ", "pəncərə", "çay", "karandaş",
            "bulud", "portağal", "körpü", "musiqi",
            "çiçək", "kitab", "dağ", "stul",
        ],
    },
}


# =========================================================
# PATTERN QUESTIONS
# =========================================================

PATTERNS = {
    "easy": [
        ((2, 4, 6, 8), 10),
        ((3, 6, 9, 12), 15),
        ((5, 10, 15, 20), 25),
        ((10, 20, 30, 40), 50),
        ((1, 3, 5, 7), 9),
    ],

    "medium": [
        ((1, 2, 4, 8), 16),
        ((2, 5, 8, 11), 14),
        ((1, 4, 9, 16), 25),
        ((3, 6, 12, 24), 48),
        ((2, 6, 18, 54), 162),
    ],

    "hard": [
        ((2, 6, 12, 20), 30),
        ((1, 1, 2, 3), 5),
        ((3, 7, 15, 31), 63),
        ((1, 4, 10, 20), 35),
        ((2, 3, 5, 9), 17),
    ],
}


# =========================================================
# DATABASE
# =========================================================

def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant TEXT DEFAULT 'DEMO-001',
            activity TEXT DEFAULT 'Unknown',
            difficulty TEXT DEFAULT 'medium',
            score INTEGER DEFAULT 0,
            max_score INTEGER DEFAULT 0,
            accuracy REAL DEFAULT 0,
            date TEXT DEFAULT ''
        )
    """)

    columns = {
        row[1] for row in
        conn.execute("PRAGMA table_info(results)").fetchall()
    }

    migrations = {
        "participant": "TEXT DEFAULT 'DEMO-001'",
        "activity": "TEXT DEFAULT 'Unknown'",
        "difficulty": "TEXT DEFAULT 'medium'",
        "score": "INTEGER DEFAULT 0",
        "max_score": "INTEGER DEFAULT 0",
        "accuracy": "REAL DEFAULT 0",
        "date": "TEXT DEFAULT ''",
    }

    for name, definition in migrations.items():
        if name not in columns:
            conn.execute(
                f"ALTER TABLE results ADD COLUMN {name} {definition}"
            )

    conn.commit()
    conn.close()


def save_result(participant, activity, level, score, maximum):
    accuracy = round(score / maximum * 100, 1) if maximum else 0

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO results
        (participant, activity, difficulty, score, max_score, accuracy, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        participant,
        activity,
        level,
        int(score),
        int(maximum),
        accuracy,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
    ))

    conn.commit()
    conn.close()

    return accuracy


def get_history(participant):
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query("""
        SELECT activity, difficulty, score, max_score, accuracy, date
        FROM results
        WHERE participant = ?
        ORDER BY id DESC
    """, conn, params=(participant,))

    conn.close()
    return df


def recommend_level(history):
    if len(history) < 3:
        return "medium", None

    average = history.head(3)["accuracy"].mean()

    if average >= 85:
        return "hard", average

    if average < 50:
        return "easy", average

    return "medium", average


# =========================================================
# THEME
# =========================================================
def apply_theme(theme):

    if theme == "Light":
        background = "#FFFFFF"
        text_color = "#000000"

    else:  # Dark Mode
        background = "#000000"
        text_color = "#FFFFFF"

    st.markdown(f"""
    <style>

    /* Main background */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {{
        background-color: {background} !important;
        color: {text_color} !important;
    }}

    /* All text */
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp p,
    .stApp span,
    .stApp label,
    .stApp li,
    .stApp div {{
        color: {text_color};
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {background} !important;
    }}

    [data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}

    /* Cards */
    .ma-card,
    [data-testid="stMetric"] {{
        background-color: {background} !important;
        color: {text_color} !important;
        border-color: {text_color} !important;
    }}

    /* Input fields */
    input,
    textarea,
    div[data-baseweb="select"] > div {{
        background-color: {background} !important;
        color: {text_color} !important;
        -webkit-text-fill-color: {text_color} !important;
    }}

    /* Radio buttons and checkboxes */
    [data-testid="stRadio"] label,
    [data-testid="stCheckbox"] label {{
        color: {text_color} !important;
    }}

    </style>
    """, unsafe_allow_html=True)

# =========================================================
# EXERCISE GENERATORS
# =========================================================

def create_memory_words(language, difficulty):
    counts = {
        "easy": 3,
        "medium": 5,
        "hard": 7,
    }

    return random.sample(
        TEXT[language]["words"],
        counts[difficulty],
    )


def create_attention_grid(difficulty):
    symbols = ["●", "▲", "■", "◆", "★"]

    settings = {
        "easy": (16, 4, 4),
        "medium": (25, 5, 7),
        "hard": (36, 6, 10),
    }

    total, columns, target_count = settings[difficulty]

    target = random.choice(symbols)
    grid = [random.choice(symbols) for _ in range(total)]

    for index in random.sample(range(total), target_count):
        grid[index] = target

    return target, grid, columns


def create_pattern_questions(difficulty):
    return random.sample(PATTERNS[difficulty], 3)


# =========================================================
# SESSION STATE
# =========================================================

def initialize_state():

    defaults = {
        "memory_round": 0,
        "memory_phase": "show",
        "memory_words": None,
        "memory_level": "medium",
        "memory_result": None,

        "attention_round": 0,
        "attention_grid": None,
        "attention_target": None,
        "attention_columns": 4,
        "attention_level": "medium",
        "attention_result": None,
        "attention_done": False,

        "pattern_round": 0,
        "pattern_questions": None,
        "pattern_level": "medium",
        "pattern_result": None,
        "pattern_done": False,

        "active_difficulty": "medium",
        "difficulty_choice": "medium",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def start_new_round(level, language):

    st.session_state.active_difficulty = level

    # Memory
    st.session_state.memory_round += 1
    st.session_state.memory_words = create_memory_words(
        language, level
    )
    st.session_state.memory_level = level
    st.session_state.memory_phase = "show"
    st.session_state.memory_result = None

    # Attention
    st.session_state.attention_round += 1

    target, grid, columns = create_attention_grid(level)

    st.session_state.attention_target = target
    st.session_state.attention_grid = grid
    st.session_state.attention_columns = columns
    st.session_state.attention_level = level
    st.session_state.attention_result = None
    st.session_state.attention_done = False

    # Pattern recognition
    st.session_state.pattern_round += 1
    st.session_state.pattern_questions = create_pattern_questions(level)
    st.session_state.pattern_level = level
    st.session_state.pattern_result = None
    st.session_state.pattern_done = False


# =========================================================
# APPLICATION START
# =========================================================

init_db()
initialize_state()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🧠 MindAge")
    st.caption("Cognitive engagement platform")

    language = st.selectbox(
        "Language / Язык / Dil",
        ["English", "Русский", "Azərbaycan dili"],
        index=1,
        key="language_choice",
    )

    t = TEXT[language]

    participant = st.text_input(
        t["participant"],
        value="DEMO-001",
        key="participant_input",
    ).strip()

    if not participant:
        participant = "DEMO-001"

    st.divider()

    page = st.radio(
        t["navigation"],
        [
            t["memory"],
            t["attention"],
            t["pattern"],
            t["history"],
        ],
        key="navigation_choice",
    )

    st.divider()
    st.caption(t["footer"])





# =========================================================
# HISTORY AND RECOMMENDATION
# =========================================================

history = get_history(participant)

recommended_level, recent_average = recommend_level(history)

level_names = {
    "easy": t["easy"],
    "medium": t["medium"],
    "hard": t["hard"],
}


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(f"""
<div class="ma-card">
    <h1>🧠 MindAge</h1>
    <p><b>{t["tagline"]}</b></p>
    <p>{t["intro"]}</p>
</div>
""", unsafe_allow_html=True)

st.info(t["notice"])


# =========================================================
# DIFFICULTY SELECTOR
# =========================================================

st.markdown("### " + t["difficulty"])

difficulty_options = ["easy", "medium", "hard"]

difficulty_labels = {
    "easy": t["easy"],
    "medium": t["medium"],
    "hard": t["hard"],
}

st.radio(
    t["difficulty"],
    options=difficulty_options,
    format_func=lambda x: difficulty_labels[x],
    horizontal=True,
    key="difficulty_choice",
    label_visibility="collapsed",
)

selected_difficulty = st.session_state.difficulty_choice

st.caption(
    f"{t['recommended']}: {level_names[recommended_level]}"
)

if recent_average is None:
    st.caption(t["not_enough"])
else:
    st.caption(
        f"{t['recommendation_note']}: {recent_average:.1f}%"
    )

if st.button(t["new_round"], key="main_new_round"):
    start_new_round(selected_difficulty, language)
    st.rerun()


difficulty = st.session_state.active_difficulty


# =========================================================
# DASHBOARD METRICS
# =========================================================

st.subheader(page)

metric_one, metric_two, metric_three = st.columns(3)

with metric_one:
    st.metric(t["total"], len(history))

with metric_two:
    average = history["accuracy"].mean() if not history.empty else 0
    st.metric(t["average"], f"{average:.1f}%")

with metric_three:
    latest = history.iloc[0]["accuracy"] if not history.empty else 0
    st.metric(t["latest"], f"{latest:.1f}%")


# =========================================================
# MEMORY TRAINING
# =========================================================

if page == t["memory"]:

    st.markdown("### " + t["memory"])
    st.write(t["memory_hint"])

    if st.session_state.memory_words is None:
        start_new_round(difficulty, language)

    words = st.session_state.memory_words
    round_id = st.session_state.memory_round

    if st.session_state.memory_phase == "show":

        st.markdown(f"""
        <div class="ma-card">
            <h2 style="text-align:center; line-height:2;">
                {"　 •　 ".join(words)}
            </h2>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            t["hide_words"],
            key=f"memory_hide_{round_id}",
        ):
            st.session_state.memory_phase = "recall"
            st.rerun()

    elif st.session_state.memory_phase == "recall":

        with st.form(key=f"memory_form_{round_id}"):

            answer = st.text_input(t["recall"])
            submitted = st.form_submit_button(t["check"])

        if submitted:

            submitted_words = {
                item.strip().casefold()
                for item in answer.split(",")
                if item.strip()
            }

            correct_words = {
                word.casefold() for word in words
            }

            score = len(
                submitted_words.intersection(correct_words)
            )

            accuracy = save_result(
                participant,
                t["memory"],
                st.session_state.memory_level,
                score,
                len(correct_words),
            )

            st.session_state.memory_result = (
                score,
                len(correct_words),
                accuracy,
            )

            st.session_state.memory_phase = "result"
            st.rerun()

    elif st.session_state.memory_phase == "result":

        score, maximum, accuracy = st.session_state.memory_result

        st.success(t["saved"])

        col1, col2 = st.columns(2)

        with col1:
            st.metric(t["score"], f"{score}/{maximum}")

        with col2:
            st.metric(t["accuracy"], f"{accuracy:.1f}%")


# =========================================================
# ATTENTION TRAINING
# =========================================================

elif page == t["attention"]:

    st.markdown("### " + t["attention"])
    st.write(t["attention_hint"])

    if st.session_state.attention_grid is None:
        start_new_round(difficulty, language)

    target = st.session_state.attention_target
    grid = st.session_state.attention_grid
    columns = st.session_state.attention_columns
    round_id = st.session_state.attention_round

    st.markdown(
        f"**{t['target']}:** "
        f"<span style='font-size:30px'>{target}</span>",
        unsafe_allow_html=True,
    )

    if not st.session_state.attention_done:

        with st.form(key=f"attention_form_{round_id}"):

            selected = []
            grid_columns = st.columns(columns)

            for index, symbol in enumerate(grid):

                with grid_columns[index % columns]:

                    checked = st.checkbox(
                        symbol,
                        key=f"attention_{round_id}_{index}",
                    )

                    if checked:
                        selected.append(index)

            submitted = st.form_submit_button(t["submit"])

        if submitted:

            correct_indices = {
                i for i, symbol in enumerate(grid)
                if symbol == target
            }

            selected_indices = set(selected)

            score = max(
                0,
                len(correct_indices & selected_indices)
                - len(selected_indices - correct_indices),
            )

            maximum = len(correct_indices)

            accuracy = save_result(
                participant,
                t["attention"],
                st.session_state.attention_level,
                score,
                maximum,
            )

            st.session_state.attention_result = (
                score,
                maximum,
                accuracy,
            )

            st.session_state.attention_done = True
            st.rerun()

    if st.session_state.attention_done:

        score, maximum, accuracy = st.session_state.attention_result

        st.success(t["saved"])

        col1, col2 = st.columns(2)

        with col1:
            st.metric(t["score"], f"{score}/{maximum}")

        with col2:
            st.metric(t["accuracy"], f"{accuracy:.1f}%")


# =========================================================
# PATTERN RECOGNITION
# =========================================================

elif page == t["pattern"]:

    st.markdown("### " + t["pattern"])
    st.write(t["pattern_hint"])

    if st.session_state.pattern_questions is None:
        start_new_round(difficulty, language)

    questions = st.session_state.pattern_questions
    round_id = st.session_state.pattern_round

    if not st.session_state.pattern_done:

        with st.form(key=f"pattern_form_{round_id}"):

            answers = []

            for index, (sequence, correct) in enumerate(
                questions,
                start=1,
            ):

                st.markdown(
                    f"**{t['question']} {index}:** "
                    + " → ".join(map(str, sequence))
                    + " → ?"
                )

                options = sorted(set([
                    correct,
                    correct + 1,
                    max(1, correct - 1),
                    correct + 2,
                ]))

                answer = st.radio(
                    f"{t['question']} {index}",
                    options,
                    key=f"pattern_{round_id}_{index}",
                    horizontal=True,
                    label_visibility="collapsed",
                )

                answers.append(answer)

            submitted = st.form_submit_button(t["submit"])

        if submitted:

            score = sum(
                1
                for answer, (_, correct) in zip(answers, questions)
                if answer == correct
            )

            accuracy = save_result(
                participant,
                t["pattern"],
                st.session_state.pattern_level,
                score,
                len(questions),
            )

            st.session_state.pattern_result = (
                score,
                len(questions),
                accuracy,
            )

            st.session_state.pattern_done = True
            st.rerun()

    if st.session_state.pattern_done:

        score, maximum, accuracy = st.session_state.pattern_result

        st.success(t["saved"])

        col1, col2 = st.columns(2)

        with col1:
            st.metric(t["score"], f"{score}/{maximum}")

        with col2:
            st.metric(t["accuracy"], f"{accuracy:.1f}%")


# =========================================================
# PROGRESS HISTORY
# =========================================================

elif page == t["history"]:

    st.markdown("### " + t["progress"])

    history = get_history(participant)

    if history.empty:

        st.info(t["no_history"])

    else:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(t["total"], len(history))

        with col2:
            st.metric(
                t["average"],
                f"{history['accuracy'].mean():.1f}%",
            )

        with col3:
            st.metric(
                t["latest"],
                f"{history.iloc[0]['accuracy']:.1f}%",
            )

        chart_data = history.iloc[::-1].copy()
        chart_data["Attempt"] = range(1, len(chart_data) + 1)

        fig, ax = plt.subplots(figsize=(9, 4))

        fig.patch.set_alpha(0)

        ax.plot(
            chart_data["Attempt"],
            chart_data["accuracy"],
            marker="o",
            linewidth=2,
        )

        ax.set_ylim(0, 100)
        ax.set_xlabel("Activity attempt")
        ax.set_ylabel("Accuracy (%)")
        ax.grid(alpha=0.25)
        ax.set_facecolor("none")

        ax.tick_params(colors="#64748B")
        ax.xaxis.label.set_color("#64748B")
        ax.yaxis.label.set_color("#64748B")

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        display = history.rename(columns={
            "activity": t["activity"],
            "difficulty": t["level"],
            "score": t["score"],
            "max_score": "Maximum",
            "accuracy": t["accuracy"] + " (%)",
            "date": t["date"],
        })

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()
st.caption(t["footer"])