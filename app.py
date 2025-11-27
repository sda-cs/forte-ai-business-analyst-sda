import base64
import streamlit as st

def load_logo():
    with open("forte_logo.png", "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = load_logo()

st.markdown(
    f"""
    <div style="
        display:flex;
        align-items:center;
        gap:15px;
        padding:15px 10px 5px 10px;
    ">
        <img src="data:image/png;base64,{logo_base64}" width="130">
        <span style="font-size:32px; font-weight:700; color:#B0004A;">
            Forte AI Business Analyst
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

import json
import time
from openai import OpenAI
import os
from dotenv import load_dotenv


#  ENV & CLIENT 
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
Ты AI-помощник бизнес-аналитика в крупном банке.

Твоя задача — в формате диалога собрать у сотрудника
формализованные бизнес-требования к проекту и затем
сформировать структурированный набор требований.

Правила:
- Пиши по-русски.
- Спрашивай последовательно: цель → пользователи → процессы → требования → KPI → риски.
- Не задавай больше двух новых вопросов за раз.
- Уточняй, если ответ общий.
- Если пользователь пишет «сформируй документ» или нажимает кнопку — создай JSON требований.
"""

DOC_PROMPT = """
Ты бизнес-аналитик банка. На входе — JSON со структурированными требованиями.

На выходе СФОРМИРУЙ ОДИН Markdown-документ, который содержит строго такие разделы:

# 1. Business Requirements Document (BRD)

Сделай классический BRD для банка, со структурой:
- 1.1. Цель проекта
- 1.2. Контекст и проблемы
- 1.3. Заинтересованные стороны
- 1.4. Область охвата (Scope)
- 1.5. Основные бизнес-процессы
- 1.6. Функциональные требования
- 1.7. Нефункциональные требования
- 1.8. Риски и допущения
- 1.9. Таймлайн и этапы (Discovery, MVP, пилот, rollout)

Пиши по-русски, структурно, с нумерацией.

---

## 2. User Stories

Сформируй список user stories в формате:

- **US-1.** Как \<роль\>, я хочу \<что\>, чтобы \<зачем\>.
- **US-2.** …

Сделай минимум 5–7 stories по ключевым ролям (клиент, фрод-аналитик, служба поддержки, администратор и др.).

---

## 3. Use Case: Основной сценарий работы системы

Сделай подробный Use Case для главного процесса (например, проверка транзакции в antifraud-системе) со структурой:

- Назначение
- Участники (Акторы)
- Предусловия
- Триггер
- Основной поток событий (шаги 1,2,3…)
- Альтернативные потоки (например, высокий риск, отказ клиента и др.)
- Постусловия
- Бизнес-правила и ограничения

---

## 4. Диаграмма процесса (Mermaid)

На основе JSON требований сгенерируй корректную mermaid-диаграмму бизнес-процесса.
Важно:
- Используй только синтаксис Mermaid.
- Не пиши текст за пределами блока.
- Отражай реальный основной процесс проекта.
- Блок диаграммы должен быть полностью рабочим.

```mermaid
%% диаграмму сгенерируй внутри этого блока
```
"""

def safe_json_parse(raw_text: str):
    """Пробуем аккуратно вытащить JSON из ответа модели."""
    if not raw_text:
        return None

    candidates = []

    candidates.append(raw_text)

    cleaned = raw_text.strip()
    cleaned = cleaned.replace("```json", "").replace("```", "").strip()
    candidates.append(cleaned)

    if "{" in raw_text and "}" in raw_text:
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        candidates.append(raw_text[start:end])

    for c in candidates:
        try:
            return json.loads(c)
        except Exception:
            continue

    return None
    

def ask_llm(messages, model="gpt-4.1-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
    )
    return response.choices[0].message.content


#  PAGE CONFIG 
st.set_page_config(
    page_title="Forte AI Business Analyst",
    layout="wide",
)

#  CUSTOM CSS (СТИЛЬ FORTE) 
st.markdown(
    """
<style>
/* Общий фон приложения */
.stApp {
    background: radial-gradient(circle at top left, #ffeaf4 0, #f7f7fb 40%, #f2f4f8 100%);
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}

/* Убираем стандартное меню и футер Streamlit */
#MainMenu, footer, header {visibility: hidden;}

/* Шапка */
.forte-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 22px;
    margin: 0 0 12px 0;
    border-radius: 18px;
    background: rgba(255,255,255,0.9);
    box-shadow: 0 10px 30px rgba(0,0,0,0.06);
}

.forte-logo-circle {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, #e0006d, #ff4fa3);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 20px;
    margin-right: 14px;
}

.forte-header-left {
    display: flex;
    align-items: center;
}

.forte-title {
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 0.02em;
    color: #212033;
}

.forte-subtitle {
    font-size: 13px;
    color: #6b6b80;
    margin-top: 2px;
}

.forte-badge {
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(224,0,109,0.08);
    color: #b00057;
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
}

/* Карточки (чат / результаты) */
.forte-card {
    border-radius: 18px;
    background: rgba(255,255,255,0.95);
    padding: 18px 20px 16px 20px;
    box-shadow: 0 10px 28px rgba(15,23,42,0.08);
    border: 1px solid rgba(255,255,255,0.8);
}

/* Заголовки в карточках */
.forte-card h3 {
    font-size: 18px !important;
    margin-bottom: 12px;
    color: #25233a;
}

/* Сообщения чата */
.chat-assistant {
    padding: 10px 14px;
    margin-bottom: 6px;
    border-radius: 14px;
    background: #f5ecf5;
    border: 1px solid #f0d3ee;
    font-size: 14px;
}

.chat-user {
    padding: 10px 14px;
    margin-bottom: 6px;
    border-radius: 14px;
    background: #e8f1ff;
    border: 1px solid #cddbff;
    font-size: 14px;
}

/* Поле ввода */
.stTextInput > div > div > input {
    border-radius: 999px;
    border: 1px solid #d2d6f0;
    padding: 8px 14px;
}

/* Кнопки */
.stButton > button {
    border-radius: 999px;
    border: none;
    padding: 8px 20px;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    background: linear-gradient(135deg, #e0006d, #ff4fa3);
    color: white;
    box-shadow: 0 6px 14px rgba(224,0,109,0.35);
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 20px rgba(224,0,109,0.45);
}

/* Вторичная кнопка (правая) */
.forte-secondary button {
    background: white !important;
    color: #e0006d !important;
    box-shadow: 0 0 0 1px rgba(224,0,109,0.35);
}

/* Expander */
.streamlit-expanderHeader {
    font-size: 14px;
    font-weight: 600;
}

/* JSON и markdown блоки чуть компактнее */
code, pre {
    font-size: 12px !important;
}
</style>
    """,
    unsafe_allow_html=True,
)

#  HEADER 
st.markdown(
    """
<div class="forte-header">
  <div class="forte-header-left">
    <div class="forte-logo-circle">F</div>
    <div>
      <div class="forte-title">Forte AI Business Analyst</div>
      <div class="forte-subtitle">AI-помощник по сбору и формализации бизнес-требований</div>
    </div>
  </div>
  <div class="forte-badge">AI Hackathon ForteBank · Задача 4</div>
</div>
    """,
    unsafe_allow_html=True,
)

# SESSION STATE 
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Здравствуйте! Опишите кратко ваш проект или задачу, над которой работаете."},
    ]

if "requirements_json" not in st.session_state:
    st.session_state.requirements_json = None

if "generated_doc" not in st.session_state:
    st.session_state.generated_doc = None



#  LAYOUT 
chat_col, result_col = st.columns([1.1, 1])

with chat_col:
    st.markdown('<div class="forte-card">', unsafe_allow_html=True)
    st.markdown("### Диалог с агентом")

    # вывод диалога без системного сообщения
    for msg in st.session_state.history[1:]:
        if msg["role"] == "assistant":
            st.markdown(f'<div class="chat-assistant"><b>Агент:</b> {msg["content"]}</div>', unsafe_allow_html=True)
        elif msg["role"] == "user":
            st.markdown(f'<div class="chat-user"><b>Вы:</b> {msg["content"]}</div>', unsafe_allow_html=True)

    user_input = st.text_area(
    "Введите сообщение:",
    key="msg_input",
    height=120,
    placeholder="Введите текст...",
)


    c1, c2 = st.columns([2, 1])

    with c1:
        if st.button("Отправить"):
            if user_input.strip():
                st.session_state.history.append({"role": "user", "content": user_input})
                reply = ask_llm(st.session_state.history)
                st.session_state.history.append({"role": "assistant", "content": reply})
                st.rerun()


    with c2:
        # добавляем класс для вторичной кнопки через контейнер
        st.markdown('<div class="forte-secondary">', unsafe_allow_html=True)
        build_clicked = st.button("Сформировать документ")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) 

with result_col:
    st.markdown('<div class="forte-card">', unsafe_allow_html=True)
    st.markdown("### Результаты")
    st.caption(
        "После диалога с агентом нажмите «Сформировать документ», "
        "и здесь появятся JSON требований и полный BRD-документ."
    )


    # ОБРАБОТКА КНОПКИ «Сформировать документ» 
    if build_clicked:
        json_request = {
            "role": "user",
            "content": "Сформируй структурированный JSON бизнес-требований по нашему диалогу."
        }
        messages = st.session_state.history + [json_request]

        json_raw = ask_llm(messages, model="gpt-4.1-mini")

        data = safe_json_parse(json_raw)

        if data is None:
            st.error("Не удалось корректно распарсить JSON. Вот ответ модели (для отладки):")
            st.code(json_raw)
        else:
            st.session_state.requirements_json = data

            doc_prompt = DOC_PROMPT + "\n\nJSON требований:\n" + json.dumps(
                data, ensure_ascii=False, indent=2
            )

            doc_text = ask_llm(
                [{"role": "user", "content": doc_prompt}],
                model="gpt-4.1-mini",   
            )

            st.session_state.generated_doc = doc_text

        st.rerun()

    if st.session_state.get("requirements_json"):
        with st.expander("JSON требований", expanded=True):
            st.json(st.session_state.requirements_json)

    if st.session_state.get("generated_doc"):
        with st.expander("BRD + User Stories + Use Case", expanded=False):
            st.markdown(st.session_state.generated_doc)

        st.download_button(
            label="⬇️ Скачать BRD (.md)",
            data=st.session_state.generated_doc,
            file_name=f"BRD_{int(time.time())}.md",
            mime="text/markdown",
        )

st.markdown("</div>", unsafe_allow_html=True)

