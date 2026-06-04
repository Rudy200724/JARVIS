# JARVIS

A multi-model voice-enabled AI assistant that combines conversational intelligence, speech processing, and system automation into a unified platform.

Inspired by the idea of interacting with computers through natural language, JARVIS bridges Large Language Models (LLMs), voice interfaces, and real-world actions. Instead of functioning as a simple chatbot, the system integrates speech recognition, text-to-speech synthesis, contextual conversations, and local task execution into a modular architecture.

---

# Table of Contents

1. [Project Overview](#1-project-overview)
2. [Why This Project Exists](#2-why-this-project-exists)
3. [Core Capabilities](#3-core-capabilities)
4. [System Architecture](#4-system-architecture)
5. [Tech Stack](#5-tech-stack)
6. [Project Structure](#6-project-structure)
7. [Quick Start](#7-quick-start)
8. [Configuration](#8-configuration)
9. [How JARVIS Works](#9-how-jarvis-works)
10. [Reliability & Failover Design](#10-reliability--failover-design)
11. [Future Roadmap](#11-future-roadmap)
12. [Known Limitations](#12-known-limitations)
13. [Inspiration](#13-inspiration)
14. [License](#14-license)

---

# 1. Project Overview

JARVIS was built as an exploration of AI system design beyond traditional chatbot interfaces.

The project focuses on combining:

* Natural language understanding
* Voice interaction
* Multi-model orchestration
* System automation
* Fault-tolerant AI pipelines

The goal is to create an assistant capable of understanding requests, reasoning about them, and taking useful actions on behalf of the user.

---

# 2. Why This Project Exists

Most AI assistants are either simple chatbots or isolated voice interfaces.

The goal of JARVIS is to explore how conversational AI, speech processing, and real-world actions can be combined into a single cohesive system.

Rather than focusing solely on model performance, the project emphasizes:

* Reliability
* System design
* Human-computer interaction
* AI integration
* Extensibility

JARVIS serves as both a personal productivity assistant and a playground for experimenting with modern AI system architectures.

---

# 3. Core Capabilities

## Conversational AI

* Natural language conversations
* Session-based conversation history
* Streaming AI responses
* Multi-turn interactions

## Voice Interface

* Real-time Speech-to-Text powered by RealtimeSTT
* Natural voice synthesis using ElevenLabs
* Hands-free interaction through voice commands

## Multi-Model Intelligence

Supports multiple LLM providers through OpenRouter:

* Gemini 2.5 Flash
* GPT-4o Mini
* DeepSeek Chat

## System Automation

Current automation capabilities include:

* Opening desktop applications
* Time and date retrieval
* Command execution through natural language

## Reliability Layer

* Automatic model failover
* Fallback between providers
* Graceful degradation during outages

---

# 4. System Architecture

```text
User Voice
    │
    ▼
RealtimeSTT
    │
    ▼
Intent Processing
    │
 ┌──┴─────────────┐
 │                │
 ▼                ▼
Automation     AI Reasoning
Layer          Engine
 │                │
 ▼                ▼
Local Actions  OpenRouter
               │
               ▼
      Gemini / GPT-4o / DeepSeek
               │
               ▼
       Response Generation
               │
               ▼
          ElevenLabs
               │
               ▼
            User
```

The assistant determines whether a request should be handled locally through automation or routed to an AI model for reasoning and response generation.

---

# 5. Tech Stack

## AI & Language Models

* OpenRouter
* Gemini 2.5 Flash
* GPT-4o Mini
* DeepSeek Chat

## Voice Processing

* RealtimeSTT
* ElevenLabs

## Core Development

* Python
* Object-Oriented Programming (OOP)
* API Integration
* Streaming Responses

## Automation

* Subprocess Management
* Desktop Application Control

---

# 6. Project Structure

```text
JARVIS/
│
├── core/
│   ├── assistant.py
│   └── brain.py
│
├── speech/
│   ├── stt.py
│   └── tts.py
│
├── tools/
│   └── system.py
│
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

## Component Responsibilities

### assistant.py

* Main assistant controller
* Voice and text mode handling
* Request lifecycle management

### brain.py

* LLM interaction layer
* Conversation history
* Model failover logic
* Streaming response generation

### stt.py

* Real-time speech recognition using RealtimeSTT

### tts.py

* Voice synthesis using ElevenLabs

### system.py

* Local automation commands
* Application launching
* Utility functions

---

# 7. Quick Start

## Prerequisites

* Python 3.10+
* OpenRouter API Key
* ElevenLabs API Key

## Clone Repository

```bash
git clone https://github.com/Rudy200724/JARVIS.git

cd JARVIS
```

## Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
OPENROUTER_KEY=your_openrouter_key
ELEVENLABS_KEY=your_elevenlabs_key
```

## Run JARVIS

```bash
python main.py
```

Choose either:

```text
text
```

or

```text
audio
```

mode when prompted.

---

# 8. Configuration

Model priority can be configured through:

```python
MODELS = [
    "google/gemini-2.5-flash",
    "openai/gpt-4o-mini",
    "deepseek/deepseek-chat-v3-0324"
]
```

JARVIS automatically switches to the next available model if the current provider fails.

---

# 9. How JARVIS Works

For every user request:

1. User speech is transcribed in real time using RealtimeSTT (audio mode).
2. Commands are checked against the automation layer.
3. If no automation command matches, the request is routed to the AI reasoning engine.
4. The request is sent through OpenRouter to the currently active model.
5. The selected model generates a streamed response.
6. Responses are synthesized into natural speech using ElevenLabs.
7. Conversation history is preserved for the current session.

This architecture keeps simple actions local while reserving LLM usage for reasoning-intensive tasks.

---

# 10. Reliability & Failover Design

Most AI assistants depend on a single provider, making them vulnerable to outages, rate limits, and service disruptions.

JARVIS implements a multi-model failover architecture:

1. Send request to the primary model.
2. Monitor for provider failures.
3. Automatically switch to the next available model.
4. Continue processing without requiring user intervention.

Current fallback chain:

```text
Gemini 2.5 Flash
        ↓
GPT-4o Mini
        ↓
DeepSeek Chat
```

This architecture improves availability and provides a more resilient user experience.

---

# 11. Future Roadmap

## Phase 1 — Memory

* Long-term memory
* User preference storage
* Conversation summarization

## Phase 2 — Knowledge Integration

* Retrieval-Augmented Generation (RAG)
* Personal knowledge base integration
* Local document search

## Phase 3 — Automation

* Browser automation
* Workflow execution
* Multi-step task planning

## Phase 4 — Autonomous Systems

* Desktop GUI
* Mobile companion application
* Agentic workflows
* Autonomous task execution

---

# 12. Known Limitations

Current limitations include:

* Limited automation command set
* No persistent memory between sessions
* No web browsing capability
* No document retrieval system
* Requires internet access for LLM inference

These limitations are intentional and are part of the planned roadmap for future versions.

---

# 13. Inspiration

Like many people interested in technology, I grew up fascinated by Tony Stark's JARVIS and the idea of interacting with computers through natural conversation.

This project is my attempt to bring a small piece of that vision into reality while exploring modern AI systems, speech interfaces, and intelligent automation.

---

# 14. License

This project is intended for educational, research, and personal use.
