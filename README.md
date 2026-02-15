# Stateful Execution Agent

A worker-like AI system capable of planning, executing, remembering, and learning from complex tasks.

## Overview

This is not a chatbot. It's an operational AI layer that:
- Breaks down complex tasks into executable steps
- Maintains state and memory across sessions
- Traces every decision with transparent reasoning
- Learns from past executions
- Acts autonomously like a worker, not reactively like a chatbot

## Architecture

### Core Components

1. **Planning Module** (`agent/planner.py`)
   - Decomposes complex tasks into manageable steps
   - Uses Google Gemini 2.5 Flash for intelligent task breakdown
   - Considers context and past experiences

2. **Execution Engine** (`agent/executor.py`)
   - Executes planned steps systematically
   - Handles various action types: document creation, analysis, content generation
   - Adapts execution based on step dependencies

3. **Memory System** (`agent/memory.py`)
   - Short-term state: current task, plan, progress
   - Long-term memory: past tasks, learned patterns, user preferences
   - Persistent storage via JSON files

4. **Decision Tracer** (`agent/tracer.py`)
   - Logs every decision with reasoning
   - Creates transparent audit trail
   - Enables trust through explainability

5. **Orchestrator** (`agent/orchestrator.py`)
   - Coordinates all components
   - Manages workflow: Planning → Execution → Completion
   - Handles state transitions and progress tracking

## Installation

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

Or set it as environment variable:
```bash
export GEMINI_API_KEY=your_key_here
```

## Usage

### Run the Agent

```bash
python main.py
```

### Available Use Cases

1. **SaaS Dashboard Launch** (Primary Scenario)
   - Creates feature specifications
   - Generates success metrics from user data
   - Develops go-to-market plans
   - Prepares team communications

2. **Quarterly Investor Update**
   - Drafts comprehensive investor reports
   - Analyzes product and growth metrics
   - Assesses risks and opportunities
   - Outlines forward-looking strategy

3. **Custom Tasks**
   - Enter your own task description
   - Provide context as needed
   - Agent plans and executes autonomously

## How It Works

### Phase 1: Planning
```
User Task → Context Retrieval → Task Decomposition → Execution Plan
```
- Agent analyzes the task
- Checks memory for similar past tasks
- Creates structured plan with dependencies
- Logs planning decisions

### Phase 2: Execution
```
For each step:
  Check Dependencies → Execute Action → Record Result → Update State
```
- Executes steps in proper order
- Respects dependencies between steps
- Logs each execution decision
- Updates memory continuously

### Phase 3: Completion
```
Collect Results → Record Learning → Save to Memory → Generate Summary
```
- Summarizes outcomes
- Stores task in long-term memory
- Makes decisions available for future tasks

## State Management

### Current Session State
Stored in `storage/agent_state.json`:
- Current task and context
- Execution plan
- Completed and pending steps
- Session ID

### Long-term Memory
Stored in `storage/long_term_memory.json`:
- Past task history
- Learned patterns
- User preferences
- Decision history

### Decision Trace
Stored in `storage/decision_trace.json`:
- Timestamped decision log
- Reasoning for each action
- Inputs and outputs
- Complete audit trail

## Decision Transparency

Every action includes:
- What decision was made
- Why it was made
- What inputs were considered
- What outputs were produced
- When it happened

Example trace output:
```
Step 1: Planning
  Action: Task decomposition
  Reasoning: Breaking down complex task into manageable steps for systematic execution
  Inputs: {task description, context}
  Outputs: {execution plan with 5 steps}

Step 2: Execution - Step 1
  Action: Create feature specification document
  Reasoning: Executing planned step to achieve: comprehensive feature documentation
  ...
```

## Example Session

```
$ python main.py

STATEFUL EXECUTION AGENT

Agent initialized. Session ID: a3f2b9c1...

Available Use Cases:
  1. SaaS Dashboard Launch (Primary Scenario)
  2. Quarterly Investor Update
  3. Custom Task (Enter your own)
  ...

Select an option: 1


STARTING NEW TASK


Task: Launch a new analytics dashboard feature...

PHASE 1: PLANNING
------------------------------------------------------------
Analyzing task and creating execution plan...

Goal: Successfully launch analytics dashboard with comprehensive documentation and metrics

Planned 5 steps:
  1. Create feature specification document
  2. Generate preliminary success metrics
  3. Draft go-to-market plan
  4. Prepare engineering team briefing
  5. Create product team communication

PHASE 2: EXECUTION
------------------------------------------------------------

Step 1/5: Create feature specification document
Description: Draft comprehensive feature specifications...
Status: completed
Output type: document

...

Task execution completed:
  Total steps: 5
  Successful: 5
  Failed: 0
```

## Key Design Decisions

1. **Stateful over Stateless**: Agent maintains context across steps and sessions
2. **Planning before Execution**: Systematic approach reduces errors
3. **Decision Transparency**: Every action is logged and explainable
4. **Simple Storage**: JSON files for quick implementation, easily upgradable to database
5. **Modular Architecture**: Each component has single responsibility
6. **Worker Mindset**: Proactive and systematic, not reactive Q&A

## Future Enhancements

- Vector database for semantic memory retrieval
- Learning from execution patterns
- Multi-agent collaboration
- Real-time streaming output
- Web-based UI
- Integration with external tools and APIs

## Technical Stack

- **LLM**: Google Gemini 2.5 Flash (via Google Gemini API)
- **Language**: Python 3.8+
- **Storage**: JSON files (upgradable to SQLite/PostgreSQL)
- **Interface**: CLI (expandable to web UI)

## Project Structure

```
stateful-agent/
├── agent/
│   ├── __init__.py
│   ├── planner.py          # Task decomposition
│   ├── executor.py         # Action execution
│   ├── memory.py           # State management
│   ├── tracer.py           # Decision logging
│   └── orchestrator.py     # Main coordination
├── use_cases/
│   ├── __init__.py
│   ├── saas_launch.py      # SaaS launch scenario
│   └── investor_update.py  # Investor update scenario
├── storage/                # State and memory files
├── outputs/                # Generated documents
├── main.py                 # CLI entry point
├── requirements.txt
└── README.md
```

## Author

Built by Kushal
February 2026
