# ✦ FinWise AI — Financial Education Assistant

A bilingual (English / 中文), source-linked financial Q&A demo for a fintech / AI operations / solutions portfolio. **Runs without an API key**, and optionally uses OpenAI to produce natural-language answers grounded in the included knowledge base.

> **Disclaimer:** Educational demo only. Not financial, tax, legal or investment advice. Not affiliated with Fidelity or another financial institution. Uses curated introductory references, not a live regulatory feed; verify current tax limits and rules directly with official sources.

## Features

- 💬 Chat-style Streamlit UI with quick question examples
- 📚 Lightweight retrieval over a local JSON knowledge base (IRA, Roth, RMD, rollovers, wash sales, mutual funds, security, FDIC/SIPC)
- 🔗 Visible reference links and uncertainty-aware responses
- 🌏 English / Chinese question support (AI mode responds in the language of the question)
- 📴 No-key offline reference mode, usable immediately
- ✨ Optional OpenAI Responses API mode, grounded in matching reference snippets
- 🔐 API key kept in environment variables / Streamlit secrets or session input; basic sensitive-data checks
- ✅ Pytest tests for retrieval and fallback

## Quick start

Requires Python 3.10+.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit (typically `http://localhost:8501`). **No API key needed.**

### Enable optional generative AI

Set the API key as an environment variable:

```bash
# macOS/Linux
export OPENAI_API_KEY="your-key-here"
# Windows PowerShell
$env:OPENAI_API_KEY="your-key-here"
```

Then toggle **Enable generative AI** in the sidebar. You can also enter a key in the app for the current session. Never commit real keys to the repo.

Model defaults to `gpt-4.1-mini` in `engine.py`; change if needed for your account. API usage may incur charges. The AI feature requires network access.

## GitHub and deployment

1. Create a public GitHub repository named `finwise-ai-assistant`.
2. Upload the contents of this project (or use `git init`, `git add .`, `git commit`, `git remote add`, `git push`).
3. To host, connect the repository to [Streamlit Community Cloud](https://share.streamlit.io/), select `app.py`, and deploy.
4. For AI mode on Streamlit Cloud, configure `OPENAI_API_KEY` under app secrets rather than in GitHub. For reference mode, no secret is required.

## How it works

```text
User question → privacy keyword check → lexical reference retrieval
                                    ├── Offline: curated answer + link
                                    └── AI mode: selected snippets → OpenAI → answer + links
```

The knowledge base is small and intentionally curated. It is **not** a live IRS lookup or full semantic/vector RAG system. Adding updated source documents, semantic embeddings, feedback telemetry, tests and an evaluation dataset would be natural next steps for production development.

## Example questions

- What is a Roth conversion?
- Can an RMD be rolled over?
- How are mutual funds priced?
- What does a wash sale mean?
- 继承 IRA 有什么 RMD 规则？

## Security & limitations

- The app does not write conversation data to disk; Streamlit manages chat history in the active user session.
- AI mode sends the question and selected educational snippets to the API provider; do not enter client data.
- The basic sensitive-data detector is **not** a comprehensive DLP system.
- Keyword retrieval can miss paraphrases and multilingual variants; a real deployment would require stronger retrieval, evaluation and human review.
- IRS rules may change, so deliberately avoid quoting annual numeric limits in static answers.

## Portfolio story

**Problem:** Client support teams answer repeated financial education questions, but responses must be understandable, traceable to sources, and conservative about account-specific advice.

**Solution:** A reference-first assistant with optional generative AI, clear provenance, basic privacy guardrails and a bilingual interface.

**Role demonstrated:** Workflow framing, reference grounding, risk identification, lightweight Python product development, test coverage and deployment readiness.

**Suggested résumé bullet:** “Built FinWise, a bilingual financial education assistant using Python, Streamlit and optional OpenAI API; designed source-linked retrieval, privacy guardrails and automated tests for retirement and brokerage FAQs.”

## License

MIT — see [LICENSE](LICENSE).
