import streamlit as st
from main_1 import prompt_chain_workflow_2
import asyncio
import time
from evaluation import evaluate_cve_id_extraction
import time
import re

#streamlit run app.py

start_message='사용자의 상황을 입력해주세요.\n\n[예시 :open5GS에서 ue가 amf에게 중복된 인증을 계속 하려고 할 때 amf에서 충돌이 일어나 이게 어떤 상황인지 알고싶어]'

prompt_chain = [
    # 1단계: CVE ID와 버전 추출
"""다음 설명에서 관련 CVE ID를 무조건 찾아주세요. 만약 CVE ID가 명시되지 않았다면, 취약점 설명과 관련된 벤더 이름, 버전 정보를 통해 유추할 수 있는 CVE ID를 제공해주세요.
- CVE ID가 명시되어 있으면 정확히 추출해주세요.
- CVE ID가 없으면 취약점 설명과 관련된 벤더 이름, 버전 정보를 통해 유추할 수 있는 CVE ID를 제공해주세요.
""",

    # 2단계: 영향 분석 (간단히)
"""위 CVE가 영향을 미치는 시스템과 그 위험성에 대해 설명해주세요.
- 이 취약점이 악용되면 어떤 피해가 발생할 수 있는지 간단히 설명해주세요.
""",

    # 3단계: 대응 방안
"""CVE ID와 이 CVE에 대한 대응 방안을 간단히 설명해주세요.
- 패치나 업그레이드 등의 대응 방법을 제시해주세요.
"""
]

# Reset 버튼
if st.button("🔄 대화 초기화"):
    st.session_state.messages = [{'role': 'assistant', 'content': start_message}]

# 제목
st.title('CVE 검색 Agent')

# 초기 메시지 설정
if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'assistant', 'content': start_message}]

# 메시지 출력
for m in st.session_state.messages:
    with st.chat_message(m['role']):
        st.write(m['content'])

# 사용자 입력 받기
if prompt := st.chat_input("CVE 관련 질문을 입력하세요:"):
    # 사용자 메시지 저장 및 표시
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)



    # 분석 실행
    with st.spinner("CVE 분석 중입니다..."):

        start_time = time.time()

        responses = prompt_chain_workflow_2(prompt, prompt_chain)

        duration = time.time() - start_time
        print(f"총 소요 시간: {duration:.2f}초")

        final_response = responses[-1]

    # 결과 출력
    st.session_state.messages.append({
        'role': 'assistant',
        'content': f"{final_response}\n\n⏱️ 총 소요 시간: {duration:.2f}초"
    })
    
    
    with st.chat_message('assistant'):
        st.markdown(f"{final_response}\n\n⏱️ 총 소요 시간: {duration:.2f}초")


# 탭 구분
tab1, tab2 = st.tabs(["CVE 검색 Agent", "📊 평가"])

with tab2:
    st.header("📊 최근 입력 기반 CVE 평가")

    # 최근 사용자 질문 찾기
    user_inputs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    ai_outputs = [m['content'] for m in st.session_state.messages if m['role'] == 'assistant']

    if not user_inputs or not ai_outputs:
        st.warning("먼저 CVE 관련 질문을 입력해야 평가할 수 있습니다.")
    else:
        latest_question = user_inputs[-1]
        latest_response = ai_outputs[-1]

        # CVE ID 추출
        predicted_id_match = re.search(r'CVE-\d{4}-\d{4,7}', latest_response)
        predicted_id = predicted_id_match.group() if predicted_id_match else ""

        st.markdown(f"**🧾 마지막 질문:** {latest_question}")
        st.markdown(f"**🤖 모델 응답 (요약):** {latest_response[:300]}...")
        st.markdown(f"**🔍 모델이 추출한 CVE ID:** `{predicted_id or '없음'}`")

        # 🔽 입력 + 제출 버튼을 폼으로 묶기
        with st.form("evaluation_form"):
            gt_input = st.text_input("✅ 정답 CVE ID를 입력해주세요 (예: CVE-2021-34527)", key="gt_input")
            submitted = st.form_submit_button("🔍 평가 실행")

        # 평가 실행
        if submitted and gt_input:
            precision, recall, f1 = evaluate_cve_id_extraction([predicted_id], [gt_input.strip()])
            st.metric("Precision", f"{precision:.2f}")
            st.metric("Recall", f"{recall:.2f}")
            st.metric("F1-score", f"{f1:.2f}")
