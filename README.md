# Multiple-Speakers-AI-Personality-Detection
This project provides an advanced AI system designed for diagnosing and profiling personality attributes from video content based on a single speaker or multiple speakers in a conversation.   

It transcribes video content, identifies speakers, and performs a comprehensive analysis of attachment styles, Big Five personality traits, and personality disorders.

## Introduction

This project loads a video file and generates a transcript with speaker identification for each of their texts. It utilizes a Large Language Model (LLM), enhanced with external knowledge input and task instructions using Retrieval-Augmented Generation (RAG) techniques to detect personality types of the different speakers involved in the video.

Additionally, the system can process and analyze interpersonal dynamics and conversations from the transcription, as each line of text is attributed to a specific speaker. This enables the LLM to identify interpersonal communication patterns and analyze them to derive meaningful psychological and personality insights.

## Features

- **Transcription & Diarization**: Uses AWS Transcribe to convert speech to text and label different speakers.
- **Personality Analysis**: Provides comprehensive analysis based on:
  - Attachment styles
  - Big Five personality traits
  - Personality disorders
- **RAG Techniques**: Employs RAG to integrate external knowledge data and task-specific instructions, enhancing the analysis accuracy.
- **Data Visualization**: Visualizes the analysis results using interactive plots and charts.
- **User-Friendly Interface**: Simple to use interface built with Gradio.


### Overview Flowchart

![Transcript Generation Workflow](appendix/AI Personality Detection flow - 1.png)

**Diarization**: Identify and label speakers in the video.
**Identify Language**: Detect the language of the conversation.
**Transcription**: Convert spoken content into written text.
**Transcript by Speakers**: Create a structured transcript with speaker labels
**Knowledge Integration**: Enhance the LLM with external knowledge about Attachments, Big Five traits, and Personalities.
**Task Definition**: Define specific tasks that guide the LLM on how to analyze the transcript.
**LLM Processing**: Use the LLM to analyze the transcript according to the tasks and integrated knowledge.
**Parse and Format Outputs**: Structure the analysis results into human-readable formats.

## Technical Flowchart

![Technical Workflow](AI Personality Detection flow - 2.png)

1. **Video Input**: A video file is input into the system.
2. **Transcription & Diarization (AWS Transcribe)**: The audio is transcribed to text, with speaker diarization to label each segment by different speakers.
3. **Embeddings & QA Retrieval**: Embeddings are generated, which are used in a question-answer retrieval system augmented by external knowledge and specific tasks.
4. **Tasks & Knowledge**: Task-specific instructions and knowledge sources are employed to guide the LLM in analyzing the transcript.
5. **LLM (ChatOpenAI)**: The Large Language Model processes the transcript using the task instructions and knowledge.
6. **Output Parsing**: The results are parsed and formatted.
7. **Results**: Final results are generated, which include visualizations and detailed analyses.

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
