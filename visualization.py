import plotly.graph_objs as go

def create_charts(results):
    charts = {}
    explanations = {}
    general_impressions = {}
    
    for speaker_id, data in results.items():
        charts[speaker_id] = {}
        explanations[speaker_id] = {}
        
        # Extract general impression
        general_impressions[speaker_id] = data.get('general_impression', "No general impression provided.")

        # Attachment Styles
        attachment_data = data['attachments']
        labels = ['Secured', 'Anxious-Preoccupied', 'Dismissive-Avoidant', 'Fearful-Avoidant']
        values = [attachment_data.secured, attachment_data.anxious_preoccupied, 
                  attachment_data.dismissive_avoidant, attachment_data.fearful_avoidant]
        
        fig = go.Figure(data=[go.Bar(x=labels, y=values, marker_color=['blue', 'orange', 'green', 'red'])])
        fig.update_layout(title=f'{speaker_id}: Attachment Styles', yaxis_range=[0, 1])
        charts[speaker_id]['attachment'] = fig
        explanations[speaker_id]['attachment'] = attachment_data.explanation
        
        # Big Five Traits
        bigfive_data = data['bigfive']
        labels = ['Extraversion', 'Agreeableness', 'Conscientiousness', 'Neuroticism', 'Openness']
        values = [bigfive_data.extraversion, bigfive_data.agreeableness, 
                  bigfive_data.conscientiousness, bigfive_data.neuroticism, bigfive_data.openness]
        
        fig = go.Figure(data=[go.Bar(x=labels, y=values, marker_color=['blue', 'green', 'red', 'purple', 'orange'])])
        fig.update_layout(title=f'{speaker_id}: Big Five Traits', yaxis_range=[0, 10])
        charts[speaker_id]['bigfive'] = fig
        explanations[speaker_id]['bigfive'] = bigfive_data.explanation
        
        # Personality Disorders
        personality_data = data['personalities']
        labels = ['Depressed', 'Paranoid', 'Schizoid-Schizotypal', 'Antisocial-Psychopathic',
                  'Borderline-Dysregulated', 'Narcissistic', 'Anxious-Avoidant', 'Dependent-Victimized', 'Obsessional']
        values = [personality_data.depressed, personality_data.paranoid,
                  personality_data.schizoid_schizotypal, personality_data.antisocial_psychopathic,
                  personality_data.borderline_dysregulated, personality_data.narcissistic,
                  personality_data.anxious_avoidant, personality_data.dependent_victimized,
                  personality_data.obsessional]
        
        fig = go.Figure(data=[go.Bar(x=labels, y=values, marker_color=['black', 'orange', 'gray', 'green', 'brown', 'purple', 'red', 'cyan', 'magenta'])])
        fig.update_layout(title=f'{speaker_id}: Personality Disorders', yaxis_range=[0, 5])
        charts[speaker_id]['personality'] = fig
        explanations[speaker_id]['personality'] = personality_data.explanation

        # Attachment Dimensions (Radar Chart)
        dimensions_data = data['attachments']
        labels = ['Avoidance', 'Self', 'Anxiety', 'Others']
        values = [dimensions_data.avoidance, dimensions_data.self_model, dimensions_data.anxiety, dimensions_data.others_model]
        
        fig = go.Figure(data=go.Scatterpolar(
          r=values,
          theta=labels,
          fill='toself',
          marker=dict(color='black'),
          line=dict(color='black')
        ))
        fig.update_layout(
          polar=dict(
            radialaxis=dict(visible=True, range=[0, 10])
          ),
          showlegend=False,
          title=f'{speaker_id}: Attachment Dimensions'
        )
        charts[speaker_id]['dimensions'] = fig

    
    return charts, explanations, general_impressions