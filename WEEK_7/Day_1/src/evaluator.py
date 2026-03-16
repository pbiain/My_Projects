"""
Evaluator module — calls the OpenAI API with the judge prompt
and parses the structured JSON response.
"""

import json
import os
import time

from openai import OpenAI

from config.config import MODEL_PRICING, JUDGE_MODEL


class Evaluator:
    def __init__(self, judge_prompt: str):
        self.judge_prompt = judge_prompt
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = JUDGE_MODEL

    def evaluate(self, response: str) -> dict:
        """
        Evaluate a chatbot response using the LLM judge.

        Args:
            response: The chatbot response text to evaluate.

        Returns:
            dict with score, reasoning, criteria_met, and metadata.
            On error, returns dict with an 'error' key.
        """
        start = time.time()

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.judge_prompt},
                    {"role": "user", "content": f"Evaluate this chatbot response:\n\n{response}"},
                ],
                temperature=0,
                response_format={"type": "json_object"},
            )
        except Exception as exc:
            return {"error": str(exc)}

        elapsed = round(time.time() - start, 2)

        raw = completion.choices[0].message.content
        try:
            result = json.loads(raw)
        except json.JSONDecodeError as exc:
            return {"error": f"JSON parse error: {exc}", "raw_response": raw}

        pricing = MODEL_PRICING.get(self.model, {"input": 0, "output": 0})
        input_tokens = completion.usage.prompt_tokens
        output_tokens = completion.usage.completion_tokens
        cost = (input_tokens * pricing["input"]) + (output_tokens * pricing["output"])

        result["metadata"] = {
            "model": self.model,
            "elapsed_time_seconds": elapsed,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": completion.usage.total_tokens,
            "estimated_cost_usd": round(cost, 6),
        }

        return result
