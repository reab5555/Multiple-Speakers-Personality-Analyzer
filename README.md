# AI-Personality-Detection
This project provides an advanced AI system designed for diagnosing and profiling personality attributes from video content using state-of-the-art NLP and transcription techniques. The system transcribes video content, identifies speakers, and performs a comprehensive analysis of attachment styles, Big Five personality traits, and personality disorders.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Configuration](#configuration)
- [Structure](#structure)
- [Contribution](#contribution)
- [License](#license)

## Introduction

This project loads a video file and generates a transcript with speaker identification for each of their texts. It utilizes a Large Language Model (LLM) artificial intelligence, enhanced with external knowledge input and task instructions using Retrieval-Augmented Generation (RAG) techniques through Langchain, to detect personality types of the different speakers involved in the video conversation.

## Features

- **Transcription & Diarization**: Uses AWS Transcribe to convert speech to text and label different speakers.
- **Personality Analysis**: Provides comprehensive analysis based on:
  - Attachment styles
  - Big Five personality traits
  - Personality disorders
- **RAG Techniques**: Employs RAG to integrate external knowledge data and task-specific instructions, enhancing the analysis accuracy.
- **Data Visualization**: Visualizes the analysis results using interactive plots and charts.
- **User-Friendly Interface**: Simple to use interface built with Gradio.

## Configuration

The project uses several configuration files to customize tasks and knowledge bases:

- **Knowledge Base Files**:
  - `knowledge/bartholomew_attachments_definitions.txt`
  - `knowledge/bigfive_definitions.txt`
  - `knowledge/personalities_definitions.txt`
- **Task Files**:
  - `tasks/general_task.txt`
  - `tasks/Attachments_task.txt`
  - `tasks/BigFive_task.txt`
  - `tasks/Personalities_task.txt`

### Customizing Tasks

You can customize the analysis tasks by modifying the files under the `tasks/` directory. These files define the specific prompts used for querying the OpenAI model.

## Structure

```
.
├── app.py
├── config.py
├── knowledge/
│   ├── bartholomew_attachments_definitions.txt
│   ├── bigfive_definitions.txt
│   └── personalities_definitions.txt
├── tasks/
│   ├── general_task.txt
│   ├── Attachments_task.txt
│   ├── BigFive_task.txt
│   └── Personalities_task.txt
└── processing.py
└── transcription_diarization.py
└── visualization.py
```
