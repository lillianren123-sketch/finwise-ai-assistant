"""FinWise: an educational financial Q&A Streamlit demo."""
import os
import re
import streamlit as st
from engine import ai_answer, load_knowledge, local_answer, retrieve

st.set_page_config(page_title="FinWise | Financial AI Assistant", page_icon="💬", layout="centered")
st.markdown("""<style>
.block-container {padding-top:2rem; max-width:830px;}
[data-testid="stChatMessage"] {border-radius:16px; padding:12px;}
.hero {background:linear-gradient(120deg,#152f43,#245b69);padding:24px;border-radius:20px;color:white;margin-bottom:22px}
.hero h1 {margin:0;color:white} .hero p {margin:9px 0 0;color:#deedf1}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>✦ FinWise AI</h1><p>Understand financial concepts with clear, source-linked answers · 金融知识咨询助手</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("About FinWise")
    st.write("A portfolio demo of retrieval-augmented financial education, with bilingual queries and source links.")
    st.info("Educational only — not individualized investment, legal or tax advice.")
    use_ai = st.toggle("Enable generative AI", help="Optional. Requires your own OpenAI API key; otherwise the reference mode works offline.")
    api_key = ""
    if use_ai:
        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            try:
                api_key = st.secrets.get("OPENAI_API_KEY", "")
            except (FileNotFoundError, KeyError):
                pass
        if not api_key:
            api_key = st.text_input("OpenAI API key (session only)", type="password", help="Do not put your API key in GitHub.")
    st.caption("This app does not store questions to disk. AI mode sends the question to an API provider.")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

knowledge = load_knowledge()
st.markdown("**Try a question**")
examples = ["What is a Roth conversion?", "How do wash sales work?", "继承 IRA 有什么 RMD 规则？", "How are mutual funds priced?"]
cols = st.columns(2)
selected = None
for i, example in enumerate(examples):
    if cols[i % 2].button(example, key=f"example_{i}", use_container_width=True):
        selected = example

if "messages" not in st.session_state:
    st.session_state.messages = []
for item in st.session_state.messages:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])
        if item.get("sources"):
            with st.expander("References / 参考来源"):
                for source in item["sources"]:
                    st.markdown(f'- [{source["title"]}]({source["url"]})')

question = st.chat_input("Ask a financial question / 用中文或英文提问...") or selected
if question:
    question = question.strip()[:1200]
    with st.chat_message("user"):
        st.write(question)
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("assistant"):
        if re.search(r"\b\d{3}-?\d{2}-?\d{4}\b|\b(?:otp|password|passcode|ssn)\s*[:=]", question, flags=re.I):
            result = {"answer": "Please remove personal identifiers, passwords or one-time codes before asking. This demonstration does not need sensitive financial information. / 请勿输入密码、验证码或个人身份信息。", "sources": [], "mode": "Safety check"}
        elif use_ai and api_key:
            try:
                result = ai_answer(question, retrieve(question, knowledge), api_key)
            except Exception:
                result = local_answer(question, knowledge)
                st.warning("AI service unavailable; showing the built-in reference answer.")
        else:
            result = local_answer(question, knowledge)
            if use_ai and not api_key:
                st.caption("Add an API key in the sidebar to enable generative AI; using reference mode for now.")
        st.markdown(result["answer"])
        st.caption(result["mode"])
        if result["sources"]:
            with st.expander("References / 参考来源", expanded=True):
                for source in result["sources"]:
                    st.markdown(f'- [{source["title"]}]({source["url"]})')
    st.session_state.messages.append({"role": "assistant", "content": result["answer"], "sources": result["sources"]})

st.divider()
st.caption("FinWise is a fictional educational demonstration, not affiliated with any financial institution. References are introductory, not a live regulatory feed. Verify all time-sensitive rules with official sources.")
