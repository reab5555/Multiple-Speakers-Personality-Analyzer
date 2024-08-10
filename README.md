# AI-Personality-Detection-v2


This project provides an advanced AI system designed for diagnosing and profiling personality attributes from video contents using state-of-the-art NLP and transcription techniques. The system transcribes video content, identifies speakers, and performs a comprehensive analysis of attachment styles, Big Five personality traits, and personality disorders.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Structure](#structure)
- [Contribution](#contribution)
- [License](#license)

## Introduction

This project leverages OpenAI’s embeddings and Boto3 for AWS S3 and Amazon Transcribe services to analyze video content, identifying speakers, and performing a thorough personality analysis. The results are visualized in a user-friendly Gradio application.

## Features

- **Transcription & Diarization**: Uses AWS Transcribe to convert speech to text and label different speakers.
- **Personality Analysis**: Provides comprehensive analysis using attachment styles, Big Five traits, and personality disorders.
- **Data Visualization**: Visualize the analysis results using interactive plots and charts.
- **User-Friendly Interface**: Simple to use interface built with Gradio.

## Installation

### Prerequisites

- Python 3.8+
- AWS Account
- OpenAI API Key

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/ai-personality-detection.git
    cd ai-personality-detection
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up configuration:
    - Create a `config.py` file in the root directory with your OpenAI and AWS credentials.

    ```python
    openai_api_key = "your-openai-api-key"
    aws_access_key_id = "your-aws-access-key-id"
    aws_secret_access_key = "your-aws-secret-access-key"
    ```

## Usage

1. Start the Gradio application:
    ```bash
    python app.py
    ```

2. Open your browser and navigate to the local host URL provided by Gradio.

3. Upload a video file, specify the maximum number of speakers, and click "Analyze".

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
