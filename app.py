import streamlit as st
import re
import random
st.set_page_config(page_title='Love youu', page_icon='<3')
@st.cache_data
def load_data():
    with open('zosiatekst.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    split_pattern_1 = r'\d+,\d+/\d+,\d+\s+pont'
    questions = re.split(split_pattern_1, content)
    questions = [question.replace('\n', ' ').replace('Visszajelzés' , '').replace('visszajelzés' , '') for question in questions]

    sections = [s.strip() for s in questions if s.strip()]



    split_pattern_2 = r'([abcd]\.|[Aa] helyes válasz:)'


    fin_all_q = []

    all_q = [re.split(split_pattern_2, section) for section in sections]

    for q in all_q:
        current = [q[0].strip()]
        for i in range(1,len(q),2):
            marker = q[i]
            content = q[i+1] if i+1 < len(q) else ''
            current.append((marker + content).strip())
        fin_all_q.append(current)    
    return fin_all_q
data = load_data()
st.title('Love you')
if 'q_index' not in st.session_state:
    st.session_state.q_index = random.randint(0, len(data)-1)
    st.session_state.show_answer = False
current_q = data[st.session_state.q_index]

st.markdown(f'### {current_q[0]}')
for option in current_q[1:]:
    if 'helyes válasz' not in option.lower():
        st.write(option)

st.divider()


# Show Answer Logic
if st.button("Helyes válasz mutatása"):
    st.session_state.show_answer = True

if st.session_state.show_answer:
    # Look for the element that contains 'helyes válasz'
    answer_text = next((item for item in current_q if "helyes válasz" in item.lower()), "Nincs megadva")
    st.success(f"**{answer_text}**")

# Next Question Logic
if st.button("Következő kérdés ➡️"):
    st.session_state.q_index = random.randint(0, len(data) - 1)
    st.session_state.show_answer = False
    st.rerun()

st.sidebar.info(f"Összes kérdés a fájlban: {len(data)}")