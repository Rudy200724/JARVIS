# JARVIS

A voice-enabled AI assistant that combines conversational intelligence, speech processing, and system automation into a unified platform.

Inspired by the idea of interacting with computers through natural language, JARVIS bridges Large Language Models (LLMs), voice interfaces, and real-world actions. Instead of functioning as a simple chatbot, the system integrates speech recognition, text-to-speech synthesis, contextual conversations, and local task execution into a modular architecture.

---

# Project Overview

JARVIS was built as an exploration of AI system design beyond traditional chatbot interfaces.

The project focuses on combining:

* Natural language understanding
* Voice interaction
* Multi-model orchestration
* System automation
* Fault-tolerant AI pipelines

The goal is to create an assistant capable of understanding requests, reasoning about them, and taking useful actions on behalf of the user.

---

# Why This Project Exists

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

# Core Capabilities

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

# System Architecture

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

# Tech Stack

## AI & Language Models

* OpenRouter for model routing and provider abstraction
* Gemini 2.5 Flash
* GPT-4o Mini
* DeepSeek Chat

## Voice Processing

* RealtimeSTT for real-time speech recognition
* ElevenLabs for low-latency voice synthesis

## Core Development

* Python
* Object-Oriented Programming (OOP)
* API Integration
* Streaming Responses

## Automation

* Subprocess Management
* Desktop Application Control

---

# Project Structure

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

# Quick Start

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

# Configuration

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

# How JARVIS Works

For every user request:

1. User speech is transcribed in real time using RealtimeSTT (audio mode).
2. Commands are checked against the automation layer.
3. If no automation command matches, the request is routed to the AI reasoning engine.
4. The request is sent through OpenRouter to the currently active model (Gemini, GPT-4o Mini, or DeepSeek).
5. The selected model generates a streamed response.
6. Responses are synthesized into natural speech using ElevenLabs.
7. Conversation history is preserved for the current session.

This architecture keeps simple actions local while reserving LLM usage for reasoning-intensive tasks.

---

# Reliability & Failover Design

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

# Future Roadmap

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

# Known Limitations

Current limitations include:

* Limited automation command set
* No persistent memory between sessions
* No web browsing capability
* No document retrieval system
* Requires internet access for LLM inference

These limitations are intentional and are part of the planned roadmap for future versions.

---

# Inspiration

Like many people interested in technology, I grew up fascinated by Tony Stark's JARVIS and the idea of interacting with computers through natural conversation.

This project is my attempt to bring a small piece of that vision into reality while exploring modern AI systems, speech interfaces, and intelligent automation.

---

# License

This project is intended for educational, research, and personal use.
