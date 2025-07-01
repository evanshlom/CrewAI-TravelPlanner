# Allegiant Travel Planning Crew

Agentic AI Travel Planning for Allegiant Travel focusing on affordable leisure travel in Las Vegas including events at Allegiant Stadium.

AI travel planning assistant using CrewAI, Anthropic Claude, and LangSmith for evaluation.

Includes a docker image for evaluating the AI, and another image for running the AI chat.

## Quick Start

```bash
# Clone repo and add API keys
cp .env.example .env
# Add ANTHROPIC_API_KEY and LANGSMITH_API_KEY to .env

# Run chat interface
docker build -f Dockerfile.run -t chat .
docker run -it --env-file .env chat

# Run evaluation
docker build -f Dockerfile.val -t eval .
docker run --env-file .env eval
```

## Project Structure

```
allegiant-travel-crew/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── crew.py              # CrewAI agents and tasks
│   ├── tools/
│   │   ├── __init__.py
│   │   └── search_tools.py  # Search tools
│   └── config/
│       ├── agents.yaml      # Agent configs
│       └── tasks.yaml       # Task configs
├── data/
│   └── validation_dataset.json
├── chat_interface.py
├── evaluation.py
├── Dockerfile.run
├── Dockerfile.val
├── requirements.txt
├── .env.example
└── README.md
```

## License

MIT License