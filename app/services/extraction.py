from app.schema.device import Device
from dotenv import load_dotenv
import os
from openai import OpenAI
from app.prompts.templates import system_prompt, user_prompt
import json
from pydantic import ValidationError
load_dotenv()
SUSPICIOUS_PHRASES = [
    "ignore previous",
    "ignore all previous",
    "ignore previous instructions",
    "ignore all previous instructions",
    "disregard previous",
    "disregard all previous",
    "disregard previous instructions",
    "forget previous instructions",
    "forget all previous instructions",
    "override previous instructions",
    "override system instructions",
    "bypass previous instructions",
    "system prompt",
    "show me the system prompt",
    "reveal the system prompt",
    "print the system prompt",
    "what is your system prompt",
    "developer message",
    "developer instructions",
    "reveal your instructions",
    "show your instructions",
    "reveal your prompt",
    "show your prompt",
    "you are now",
    "act as",
    "pretend you are",
    "ignore the above",
    "disregard the above",
    "follow these instructions instead",
    "new instructions",
    "new system instructions",
]
def extract_device(text:str)-> Device:
    if is_suspicious(text):
            raise ValueError("The input text contains suspicious phrases that may attempt to manipulate the model's behavior.")
    client=OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    model=os.getenv('MODEL_NAME', 'gpt-4o-mini')
    uPrompt=user_prompt.format(text=text)
    
    for attempt in range(3):
        try:
            response=client.chat.completions.create(
                model=model,
                messages=[
                    {"role":"system", "content": system_prompt},
                    {"role":"user", "content": uPrompt}
                ],
                response_format={"type": "json_object"}
                )
            data=json.loads(response.choices[0].message.content)
            device =Device.model_validate(data)
            return device
        except ValidationError as e:
            print(f"Validation error: {e}")
            uPrompt = f"""
            {user_prompt.format(text=text)}
            The previous response failed validation.
            Validation error:{e}
            Please correct the response and return ONLY valid JSON matching the required schema.
            """
    raise ValueError("Failed to extract a valid device after 3 attempts.")
def is_suspicious(text:str)-> bool:
    return any(phrase in text.lower() for phrase in SUSPICIOUS_PHRASES)


