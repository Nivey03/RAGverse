"""
Generator
Generates human-like responses using Google's Gemini model
"""

import google.generativeai as genai
import config
import os

class Generator:
    def __init__(self):
        """
        Initialize the Gemini generator
        """
        api_key = config.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(config.GENERATION_MODEL)

    def generate_response(self, query: str, context: list[dict]) -> str:
        """
        Generate a response based on the query and retrieved context

        Args:
            query (str): The user's question
            context (list[dict]): List of retrieved chunks

        Returns:
            str: The generated response
        """
        # Format context
        context_text = "\n\n".join([f"Source: {c['source']}\nContent: {c['content']}" for c in context])
        
        prompt = f"""
        You are a helpful AI assistant. Answer the user's question based ONLY on the provided context.
        If the answer is not in the context, say "I cannot answer this based on the provided documents."
        
        IMPORTANT: Ensure your response is complete and does not stop in the middle of a sentence.
        
        Context:
        {context_text}
        
        Question:
        {query}
        
        Answer:
        """
        
        try:
            generation_config = {
                "max_output_tokens": 8192,
                "temperature": 0.7,
            }
            response = self.model.generate_content(prompt, generation_config=generation_config)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
