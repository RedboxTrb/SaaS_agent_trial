# Stateful Execution Agent

A worker-like system that plans, executes, and learns from complex multi-step tasks.

## What It Does

This agent operates autonomously by:
- Breaking down tasks into executable steps
- Maintaining state across sessions
- Logging every decision with reasoning
- Learning from past executions

## Installation

```bash
pip install -r requirements.txt
```

Requires Python 3.8+ and a Google Gemini API key.

## Usage

```bash
python main.py
```

The agent will run the SaaS Dashboard Launch scenario, which includes:
- Creating feature specifications
- Generating success metrics
- Drafting go-to-market plans
- Preparing team communications

## Architecture

Five core components work together:

1. **Planner** - Breaks tasks into steps
2. **Executor** - Runs each action
3. **Memory** - Manages state (short-term + long-term)
4. **Tracer** - Logs decisions with reasoning
5. **Orchestrator** - Coordinates everything

State is persisted to JSON files in `storage/`. Generated outputs go to `outputs/`.

## Project Structure

```
├── agent/              # Core modules
├── use_cases/          # Task scenarios
├── main.py             # Entry point
├── requirements.txt
└── META_COMMENTARY.txt # Design decisions and details
```

## Documentation

See `META_COMMENTARY.txt` for:
- Architecture decisions and reasoning
- State flow between tasks
- Implementation details
- Evaluation criteria alignment

## Technical Stack

- Google Gemini 2.5 Flash
- Python 3.8+
- JSON file storage

---

Built by Kushal, February 2026
