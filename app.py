import gradio as gr
from llm_loader import load_model
from processing import process_input
from transcription_diarization import diarize_audio
from visualization import create_charts
import time
import re
import cv2
import os
from config import openai_api_key

# Load the model
llm = load_model(openai_api_key)

def analyze_video(video_path, progress=gr.Progress()):
    start_time = time.time()
    if not video_path:
        return [None] * 29  # Return None for all outputs

    progress(0, desc="Starting analysis...")
    progress(0.2, desc="Starting transcription and diarization")
    transcription = diarize_audio(video_path)
    progress(0.5, desc="Transcription and diarization complete.")

    progress(0.6, desc="Processing transcription")
    results = process_input(transcription, llm)
    progress(0.7, desc="Transcription processing complete.")

    progress(0.9, desc="Generating charts")
    charts, explanations, general_impressions = create_charts(results)

    progress(1.0, desc="Charts generation complete.")
    
    end_time = time.time()
    execution_time = end_time - start_time

    output_components = []  # transcript

    output_components.append(f"Completed in {int(execution_time)} seconds.")
    output_components.append(gr.Textbox(value=transcription, label="Transcript", lines=10, visible=True))
                
    for i, (speaker_id, speaker_charts) in enumerate(charts.items(), start=1):
        print(speaker_id)
        speaker_explanations = explanations[speaker_id]
        speaker_general_impression = general_impressions[speaker_id]
        
        with gr.Tab(visible=True):
            with gr.TabItem(label=f'General Impression'):
                speaker_section1 = [
                    gr.Markdown(f"### {speaker_id}", visible=True),
                    gr.Textbox(value=speaker_general_impression, label="General Impression", visible=True, lines=10)
                ]

            with gr.TabItem(label=f'Attachment Styles'):
                speaker_section2 = [
                    gr.Plot(value=speaker_charts.get("attachment", None), visible=True),
                    gr.Plot(value=speaker_charts.get("dimensions", None), visible=True),
                    gr.Textbox(value=speaker_explanations.get("attachment", ""), label="Attachment Styles Explanation",
                               visible=True, lines=2)
                ]

            with gr.TabItem(label=f'Big Five Traits'):
                speaker_section3 = [
                    gr.Plot(value=speaker_charts.get("bigfive", None), visible=True),
                    gr.Textbox(value=speaker_explanations.get("bigfive", ""), label="Big Five Traits Explanation",
                               visible=True, lines=2)
                ]

            with gr.TabItem(label=f'Personalities'):
                speaker_section4 = [
                    gr.Plot(value=speaker_charts.get("personality", None), visible=True),
                    gr.Textbox(value=speaker_explanations.get("personality", ""),
                               label="Personality Disorders Explanation", visible=True, lines=2)
                ]

        output_components.extend(speaker_section1)
        output_components.extend(speaker_section2)
        output_components.extend(speaker_section3)
        output_components.extend(speaker_section4)

    # Pad with None for any missing speakers
    while len(output_components) < 28:
        output_components.extend([gr.update(visible=False)] * 9)

    return output_components



with gr.Blocks() as iface:
    gr.Markdown("# Multiple Speakers Personality Analyzer")
    gr.Markdown("This project provides an advanced AI system designed for diagnosing and profiling personality attributes from video content based on a single speaker or multiple speakers in a conversation.")

    with gr.Row():
        video_input = gr.Video(label="Upload Video")
    
    analyze_button = gr.Button("Analyze")
            
    # Create output components
    output_components = []
    # Add transcript output near the top
    execution_box = gr.Textbox(label="Execution Info", value="N/A", lines=1)
    output_components.append(execution_box)

    transcript = gr.Textbox(label="Transcript", lines=10, visible=False)
    output_components.append(transcript)
                
    with open('description.txt', 'r') as file:
        description_txt = file.read()
                
    for n in range(3):  # Assuming maximum of 3 speakers
        with gr.Tab(label=f'Speaker {n + 1}', visible=True):
            with gr.TabItem(label=f'General Impression'):
                column_components1 = [
                    gr.Markdown(visible=False),
                    gr.Textbox(label="General Impression")]

            with gr.TabItem(label=f'Attachment Styles'):
                column_components2 = [
                    gr.Plot(visible=False),
                    gr.Plot(visible=False),
                    gr.Textbox(label="Attachment Styles Explanation")]

            with gr.TabItem(label=f'Big Five Traits'):
                column_components3 = [
                    gr.Plot(visible=False),
                    gr.Textbox(label="Big Five Traits Explanation")]

            with gr.TabItem(label=f'Personalities'):
                column_components4 = [
                    gr.Plot(visible=False),
                    gr.Textbox(label="Personality Disorders Explanation")]

        output_components.extend(column_components1)
        output_components.extend(column_components2)
        output_components.extend(column_components3)
        output_components.extend(column_components4)


    gr.HTML("<div style='height: 20px;'></div>")        
    gr.Markdown(description_txt)
    gr.HTML("<div style='height: 20px;'></div>")
    gr.Image(value="appendix/AI Personality Detection flow - 1.png", label='Flowchart 1', width=900)
    gr.Image(value="appendix/AI Personality Detection flow - 2.png", label='Flowchart 2', width=900)

    analyze_button.click(
        fn=analyze_video,
        inputs=[video_input],
        outputs=output_components,
        show_progress=True
    )


if __name__ == "__main__":
    iface.launch()