from langchain.schema import HumanMessage, BaseRetriever, Document
from output_parser import output_parser
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from llm_loader import load_model, count_tokens
from config import openai_api_key
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from typing import List, Any, Optional
from pydantic import Field
from langchain_core.callbacks import CallbackManagerForRetrieverRun
import os
import json

# Initialize embedding model
embedding_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Define knowledge files
knowledge_files = {
    "attachments": "knowledge/bartholomew_attachments_definitions.txt",
    "bigfive": "knowledge/bigfive_definitions.txt",
    "personalities": "knowledge/personalities_definitions.txt"
}

# Load text-based knowledge
documents = []
for key, file_path in knowledge_files.items():
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip()
        documents.append(content)

# Create FAISS index from text documents
text_faiss_index = FAISS.from_texts(documents, embedding_model)

# Load pre-existing FAISS indexes
attachments_faiss_index = FAISS.load_local("knowledge/faiss_index_Attachments_db", embedding_model, allow_dangerous_deserialization=True)
personalities_faiss_index = FAISS.load_local("knowledge/faiss_index_Personalities_db", embedding_model, allow_dangerous_deserialization=True)

# Initialize LLM
llm = load_model(openai_api_key)

# Create retrievers for each index
text_retriever = text_faiss_index.as_retriever()
attachments_retriever = attachments_faiss_index.as_retriever()
personalities_retriever = personalities_faiss_index.as_retriever()

class CombinedRetriever(BaseRetriever):
    retrievers: List[BaseRetriever] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(
        self, query: str, *, run_manager: Optional[CallbackManagerForRetrieverRun] = None
    ) -> List[Document]:
        combined_docs = []
        for retriever in self.retrievers:
            docs = retriever.get_relevant_documents(query, run_manager=run_manager)
            combined_docs.extend(docs)
        return combined_docs

    async def _aget_relevant_documents(
        self, query: str, *, run_manager: Optional[CallbackManagerForRetrieverRun] = None
    ) -> List[Document]:
        combined_docs = []
        for retriever in self.retrievers:
            docs = await retriever.aget_relevant_documents(query, run_manager=run_manager)
            combined_docs.extend(docs)
        return combined_docs

# Create an instance of the combined retriever
combined_retriever = CombinedRetriever(retrievers=[text_retriever, attachments_retriever, personalities_retriever])

# Create prompt template for query generation
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="Generate multiple search queries for the following question: {question}"
)

# Create query generation chain
query_generation_chain = prompt_template | llm

# Create multi-query retrieval chain
def generate_queries(input):
    queries = query_generation_chain.invoke({"question": input}).content.split('\n')
    return [query.strip() for query in queries if query.strip()]

def multi_query_retrieve(input):
    queries = generate_queries(input)
    all_docs = []
    for query in queries:
        docs = combined_retriever.get_relevant_documents(query)
        all_docs.extend(docs)
    return all_docs

multi_query_retriever = RunnableLambda(multi_query_retrieve)

# Create QA chain with multi-query retriever
qa_chain = (
    {"context": multi_query_retriever, "question": RunnablePassthrough()}
    | prompt_template
    | llm
)

def load_text(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def truncate_text(text: str, max_tokens: int = 16000) -> str:
    words = text.split()
    if len(words) > max_tokens:
        return ' '.join(words[:max_tokens])
    return text

def process_input(input_text: str, llm):
    general_task = load_text("tasks/General_tasks_description.txt")
    general_impression_task = load_text("tasks/General_Impression_task.txt")
    attachments_task = load_text("tasks/Attachments_task.txt")
    bigfive_task = load_text("tasks/BigFive_task.txt")
    personalities_task = load_text("tasks/Personalities_task.txt")

    truncated_input = truncate_text(input_text)

    relevant_docs = qa_chain.invoke({"query": truncated_input})
    
    retrieved_knowledge = str(relevant_docs)

    prompt = f"""
{general_task}
Genral Impression Task:
{general_impression_task}
Attachment Styles Task:
{attachments_task}
Big Five Traits Task:
{bigfive_task}
Personality Disorders Task:
{personalities_task}
Retrieved Knowledge: {retrieved_knowledge}
Input: {truncated_input}
Please provide a comprehensive analysis for each speaker, including:
1. General impressions (answer the sections provided in the General Impression Task.)
2. Attachment styles (use the format from the Attachment Styles Task)
3. Big Five traits (use the format from the Big Five Traits Task)
4. Personality disorders (use the format from the Personality Disorders Task)
Respond with a JSON object containing an array of speaker analyses under the key 'speaker_analyses'. Each speaker analysis should include all four aspects mentioned above, however, General impressions must not be in json or dict format.
Analysis:"""

    #truncated_input_tokents_count = count_tokens(truncated_input)
    #print('truncated_input_tokents_count:', truncated_input_tokents_count)
    #input_tokens_count = count_tokens(prompt)
    #print('input_tokens_count', input_tokens_count)
    
    response = llm.invoke(prompt)
    
    print("Raw LLM Model Output:")
    print(response.content)

    try:
        content = response.content
        if content.startswith("```json"):
            content = content.split("```json", 1)[1]
        if content.endswith("```"):
            content = content.rsplit("```", 1)[0]
        
        parsed_json = json.loads(content.strip())
        
        results = {}
        speaker_analyses = parsed_json.get('speaker_analyses', [])
        for i, speaker_analysis in enumerate(speaker_analyses, 1):
            speaker_id = f"Speaker {i}"
            parsed_analysis = output_parser.parse_speaker_analysis(speaker_analysis)

                # Convert general_impression to string if it's a dict or JSON object
            general_impression = parsed_analysis.general_impression
            if isinstance(general_impression, dict):
                general_impression = json.dumps(general_impression)
            elif isinstance(general_impression, str):
                try:
                    # Check if it's a JSON string
                    json.loads(general_impression)
                    # If it parses successfully, it's likely a JSON string, so we'll keep it as is
                except json.JSONDecodeError:
                    # If it's not a valid JSON string, we'll keep it as is (it's already a string)
                    pass
            
            results[speaker_id] = {
                'general_impression': general_impression,
                'attachments': parsed_analysis.attachment_style,
                'bigfive': parsed_analysis.big_five_traits,
                'personalities': parsed_analysis.personality_disorder
            }
        
        if not results:
            print("Warning: No speaker analyses found in the parsed JSON.")
            empty_analysis = output_parser.parse_speaker_analysis({})
            return {"Speaker 1": {
                'general_impression': empty_analysis.general_impression,
                'attachments': empty_analysis.attachment_style,
                'bigfive': empty_analysis.big_five_traits,
                'personalities': empty_analysis.personality_disorder
            }}
        
        return results
    except Exception as e:
        print(f"Error processing input: {e}")
        empty_analysis = output_parser.parse_speaker_analysis({})
        return {"Speaker 1": {
            'general_impression': empty_analysis.general_impression,
            'attachments': empty_analysis.attachment_style,
            'bigfive': empty_analysis.big_five_traits,
            'personalities': empty_analysis.personality_disorder
        }}