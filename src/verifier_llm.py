import json
from openai import OpenAI
import os

class FactChecker:
    def __init__(self):
       
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama" 
        )
        
       
        self.model_name = "mistral" 

    def verify_claim(self, claim, evidence_list):
        evidence_text = "\n".join([f"- {idx+1}. {fact}" for idx, fact in enumerate(evidence_list)])
        
        system_prompt = """
        You are a strict fact-checking assistant. You will be given a USER CLAIM and a list of RETRIEVED FACTS (Evidence).
        
        Your Goal: Determine if the claim is True, False, or Unverifiable based ONLY on the provided evidence.
        
        Output Format: JSON only.
        {
            "verdict": "✅ True" | "❌ False" | "🤷‍♂️ Unverifiable",
            "reasoning": "Concise explanation comparing specific details."
        }
        
        Rules:
        1. If evidence explicitly confirms the claim, return True.
        2. If evidence explicitly contradicts the claim, return False.
        3. If the evidence is unrelated or insufficient, return Unverifiable.
        """

        user_prompt = f"""
        User Claim: "{claim}"
        
        Retrieved Evidence:
        {evidence_text}
        """

        try:
           
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
               
                response_format={"type": "json_object"},
                temperature=0
            )
            
            final_result = json.loads(response.choices[0].message.content)
            final_result["evidence"] = evidence_list 
            return final_result

        except Exception as e:
            return {
                "verdict": "Error",
                "reasoning": f"Local LLM Error: {str(e)}. Is Ollama running?",
                "evidence": evidence_list
            }
