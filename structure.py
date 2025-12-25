

# AI-Study-Assistant/
# │
# ├── backend/
# │   ├── app/
# │   │   ├── main.py                 # FastAPI entry point
# │   │   ├── api/
# │   │   │   ├── routes/
# │   │   │   │   ├── chat.py          # Chat endpoints
# │   │   │   │   ├── upload.py        # PDF/image upload
# │   │   │   │   ├── exam.py          # Exam session endpoints
# │   │   │   │   └── news.py          # Current affairs
# │   │   │   └── deps.py              # Dependencies
# │   │   │
# │   │   ├── agents/
# │   │   │   ├── orchestrator.py      # LangGraph controller
# │   │   │   ├── chat_agent.py        # Normal chatting
# │   │   │   ├── explanation_agent.py # Topic explanation
# │   │   │   ├── exam_agent.py        # Question flow logic
# │   │   │   ├── evaluation_agent.py  # Answer evaluation
# │   │   │   ├── feedback_agent.py    # Mistake explanation
# │   │   │   └── news_agent.py        # Live info agent
# │   │   │
# │   │   ├── graph/
# │   │   │   ├── state.py             # TypedDict / Pydantic state
# │   │   │   ├── nodes.py             # LangGraph nodes
# │   │   │   ├── edges.py             # Conditional routing
# │   │   │   └── graph.py             # Graph compilation
# │   │   │
# │   │   ├── services/
# │   │   │   ├── llm_service.py       # Groq client wrapper
# │   │   │   ├── ocr_service.py       # Image preprocessing + OCR
# │   │   │   ├── pdf_service.py       # PDF parsing
# │   │   │   ├── embedding_service.py # Vector embeddings
# │   │   │   └── retrieval_service.py # RAG logic
# │   │   │
# │   │   ├── tools/
# │   │   │   ├── prompt_templates.py  # Centralized prompts
# │   │   │   ├── scoring.py           # Evaluation rubric
# │   │   │   └── utils.py             # Helpers
# │   │   │
# │   │   ├── models/
# │   │   │   ├── exam.py              # Question / Answer schemas
# │   │   │   ├── student.py           # Student state tracking
# │   │   │   └── document.py          # Parsed content
# │   │   │
# │   │   ├── storage/
# │   │   │   ├── vector_db/            # FAISS / Chroma
# │   │   │   └── uploads/              # PDFs & images
# │   │   │
# │   │   ├── config/
# │   │   │   ├── settings.py          # Env & config
# │   │   │   └── constants.py
# │   │   │
# │   │   └── tests/
# │   │       ├── test_agents.py
# │   │       ├── test_exam_flow.py
# │   │       └── test_ocr.py
# │   │
# │   ├── Dockerfile
# │   ├── requirements.txt
# │   └── .env
# │
# ├── frontend/                        # Optional but inevitable
# │   ├── src/
# │   └── package.json
# │
# ├── docs/
# │   ├── architecture.md
# │   ├── agent_flows.md
# │   └── evaluation_logic.md
# │
# ├── scripts/
# │   ├── ingest_documents.py
# │   └── seed_questions.py
# │
# ├── .gitignore
# ├── README.md
# └── docker-compose.yml












#             ┌───────────────┐
#             │   START       │
#             └──────┬────────┘
#                    │
#           ┌────────▼─────────┐
#           │ Orchestrator     │  decides mode
#           │ (route by mode)  │
#           └──────┬───────────┘
#      ┌────────────┼──────────────┐
#      │            │              │
# ┌────▼────┐  ┌────▼────┐   ┌─────▼─────┐
# │ Chat    │  │Explain  │   │ Exam Mode │
# │ Agent   │  │ Agent   │   │ Controller│
# └────┬────┘  └────┬────┘   └─────┬─────┘
#      │            │              │
#      ▼            ▼      ┌───────▼────────┐
#    END          END      │ Ask Question    │
#                           └───────┬────────┘
#                                   ▼
#                          ┌────────▼─────────┐
#                          │ Student Answer   │
#                          └────────┬─────────┘
#                                   ▼
#                          ┌────────▼─────────┐
#                          │ Evaluation Agent │
#                          └────────┬─────────┘
#                                   ▼
#                          ┌────────▼─────────┐
#                          │ Feedback Agent   │
#                          └────────┬─────────┘
#                                   ▼
#                          ┌────────▼─────────┐
#                          │ Ready for next?  │
#                          └──────┬─────┬─────┘
#                                 │yes  │no
#                                 ▼     ▼
#                          Ask next Q   Explain again
