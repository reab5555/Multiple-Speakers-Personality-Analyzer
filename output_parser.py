from typing import List, Optional
from pydantic import BaseModel, Field
import json

class AttachmentStyle(BaseModel):
    secured: float = 0.0
    anxious_preoccupied: float = 0.0
    dismissive_avoidant: float = 0.0
    fearful_avoidant: float = 0.0
    avoidance: int = 0
    self_model: int = 0
    anxiety: int = 0
    others_model: int = 0
    explanation: str = "No explanation provided"

class BigFiveTraits(BaseModel):
    extraversion: int = 0
    agreeableness: int = 0
    conscientiousness: int = 0
    neuroticism: int = 0
    openness: int = 0
    explanation: str = "No explanation provided"

class PersonalityDisorder(BaseModel):
    depressed: int = 0
    paranoid: int = 0
    schizoid_schizotypal: int = 0
    antisocial_psychopathic: int = 0
    borderline_dysregulated: int = 0
    narcissistic: int = 0
    anxious_avoidant: int = 0
    dependent_victimized: int = 0
    obsessional: int = 0
    explanation: str = "No explanation provided"

class SpeakerAnalysis(BaseModel):
    speaker: str = "Unknown Speaker"
    general_impression: str = "No general impression provided"
    attachment_style: AttachmentStyle = AttachmentStyle()
    big_five_traits: BigFiveTraits = BigFiveTraits()
    personality_disorder: PersonalityDisorder = PersonalityDisorder()

class OutputParser:
    def parse(self, text: str) -> List[SpeakerAnalysis]:
        try:
            data = json.loads(text)
            if "speaker_analyses" in data and isinstance(data["speaker_analyses"], list):
                return [self.parse_speaker_analysis(item) for item in data["speaker_analyses"]]
            else:
                raise ValueError("Invalid JSON structure: missing or invalid 'speaker_analyses' key")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON: {text}")
        except Exception as e:
            raise ValueError(f"Error parsing output: {str(e)}")

    def parse_speaker_analysis(self, obj: dict) -> SpeakerAnalysis:
        attachment_styles = obj.get("Attachment Styles", {})
        big_five_traits = obj.get("Big Five Traits", {})
        personality_disorders = obj.get("Personality Disorders", {})
    
        # Handle general_impression as a string
        general_impression = obj.get("General Impression", {})
        if isinstance(general_impression, dict):
            # Convert the dictionary to a formatted string
            general_impression_str = "\n".join([f"{key}: {value}" for key, value in general_impression.items()])
        else:
            general_impression_str = str(general_impression)
    
        return SpeakerAnalysis(
            speaker=str(obj.get("Speaker", "Unknown Speaker")),  # Convert to string
            general_impression=general_impression_str,
            attachment_style=AttachmentStyle(
                secured=attachment_styles.get("Secured", 0.0),
                anxious_preoccupied=attachment_styles.get("Anxious-Preoccupied", 0.0),
                dismissive_avoidant=attachment_styles.get("Dismissive-Avoidant", 0.0),
                fearful_avoidant=attachment_styles.get("FearfulAvoidant", 0.0),
                avoidance=attachment_styles.get("Avoidance", 0),
                self_model=attachment_styles.get("Self", 0),
                anxiety=attachment_styles.get("Anxiety", 0),
                others_model=attachment_styles.get("Others", 0),
                explanation=attachment_styles.get("Explanation", "No explanation provided")
            ),
            big_five_traits=BigFiveTraits(
                extraversion=big_five_traits.get("Extraversion", 0),
                agreeableness=big_five_traits.get("Agreeableness", 0),
                conscientiousness=big_five_traits.get("Conscientiousness", 0),
                neuroticism=big_five_traits.get("Neuroticism", 0),
                openness=big_five_traits.get("Openness", 0),
                explanation=big_five_traits.get("Explanation", "No explanation provided")
            ),
            personality_disorder=PersonalityDisorder(
                depressed=personality_disorders.get("Depressed", 0),
                paranoid=personality_disorders.get("Paranoid", 0),
                schizoid_schizotypal=personality_disorders.get("Schizoid-Schizotypal", 0),
                antisocial_psychopathic=personality_disorders.get("Antisocial-Psychopathic", 0),
                borderline_dysregulated=personality_disorders.get("Borderline-Dysregulated", 0),
                narcissistic=personality_disorders.get("Narcissistic", 0),
                anxious_avoidant=personality_disorders.get("Anxious-Avoidant", 0),
                dependent_victimized=personality_disorders.get("Dependent-Victimized", 0),
                obsessional=personality_disorders.get("Obsessional", 0),
                explanation=personality_disorders.get("Explanation", "No explanation provided")
            )
        )

output_parser = OutputParser()