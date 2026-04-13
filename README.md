🌐 [Português (BR)](README.pt_BR.md) | [Español](README.es.md)

<div align="center">

# 🎯 Soc Ops

**Break the ice. Fill the board. Call BINGO!**

Soc Ops is a social bingo game built for in-person mixers, team events, and conferences. Mingle with the crowd, find people who match each square, and race to complete a line of five.

*Built with FastAPI · Jinja2 · HTMX — zero JavaScript frameworks required.*

</div>

---

## ✨ How It Works

1. **Start a game** — you get a shuffled 5×5 board of icebreaker prompts.
2. **Talk to people** — find someone who *bikes to work*, *plays an instrument*, or *has a hidden talent*.
3. **Tap the square** — mark it off when you find a match.
4. **Get five in a row** — any row, column, or diagonal wins. The center square is free!

---

## 🚀 Quick Start

```bash
# install dependencies
uv sync

# start the dev server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open **http://localhost:8000** in your browser.

---

## 🧪 Development

```bash
uv run ruff check .   # lint
uv run pytest          # test
```

### Project Layout

```
app/
├── main.py          # FastAPI routes (thin handlers)
├── game_service.py  # Session state & transitions
├── game_logic.py    # Board generation & bingo detection
├── models.py        # Pydantic models & enums
├── data.py          # Icebreaker prompts
├── templates/       # Jinja2 templates (HTMX partials)
└── static/          # CSS utilities & HTMX client
```

---

## 📚 Lab Guide

This repo powers a hands-on workshop. Follow the parts below or browse the [`workshop/`](workshop/) folder offline.

| Part | Title |
|------|-------|
| [**00**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=00-overview) | Overview & Checklist |
| [**01**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=01-setup) | Setup & Context Engineering |
| [**02**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=02-design) | Design-First Frontend |
| [**03**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=03-quiz-master) | Custom Quiz Master |
| [**04**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=04-multi-agent) | Multi-Agent Development |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
