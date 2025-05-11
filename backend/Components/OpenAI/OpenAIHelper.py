import os
from openai import OpenAI
import time
from typing import List, Optional, Dict, Any

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)

def generate_chat_completion(messages: List[Dict[str, str]], model: str = "gpt-4") -> str:
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error generating chat completion: {str(e)}")

def generate_text_completion(prompt: str, model: str = "gpt-3.5-turbo-instruct") -> str:
    try:
        client = get_openai_client()
        response = client.completions.create(
            model=model,
            prompt=prompt
        )
        return response.choices[0].text
    except Exception as e:
        raise Exception(f"Error generating text completion: {str(e)}")

def upload_file(file_path: str, purpose: str = "assistants") -> str:
    try:
        client = get_openai_client()
        with open(file_path, "rb") as file:
            response = client.files.create(
                file=file,
                purpose=purpose
            )
        return response.id
    except Exception as e:
        raise Exception(f"Error uploading file: {str(e)}")

def create_assistant(
    name: str, 
    instructions: str, 
    model: str = "gpt-4", 
    file_ids: Optional[List[str]] = None,
    tools: Optional[List[Dict[str, Any]]] = None
) -> str:
    try:
        client = get_openai_client()
        
        create_params = {
            "name": name,
            "instructions": instructions,
            "model": model
        }
        
        if file_ids:
            create_params["file_ids"] = file_ids
            
        if tools:
            create_params["tools"] = tools
        
        assistant = client.beta.assistants.create(**create_params)
        return assistant.id
    except Exception as e:
        raise Exception(f"Error creating assistant: {str(e)}")

def create_thread() -> str:
    try:
        client = get_openai_client()
        thread = client.beta.threads.create()
        return thread.id
    except Exception as e:
        raise Exception(f"Error creating thread: {str(e)}")

def add_message_to_thread(
    thread_id: str, 
    content: str, 
    file_ids: Optional[List[str]] = None
) -> str:
    try:
        client = get_openai_client()
        message_params = {
            "role": "user",
            "content": content
        }
        
        if file_ids:
            message_params["file_ids"] = file_ids
            
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            **message_params
        )
        return message.id
    except Exception as e:
        raise Exception(f"Error adding message to thread: {str(e)}")

def run_assistant(
    thread_id: str, 
    assistant_id: str,
    instructions: Optional[str] = None
) -> str:
    try:
        client = get_openai_client()
        run_params = {"assistant_id": assistant_id}
        
        if instructions:
            run_params["instructions"] = instructions
            
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            **run_params
        )
        return run.id
    except Exception as e:
        raise Exception(f"Error running assistant: {str(e)}")

def wait_for_run_completion(thread_id: str, run_id: str, poll_interval: float = 1.0) -> str:
    try:
        client = get_openai_client()
        while True:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )
            if run.status in ["completed", "failed", "cancelled", "expired"]:
                return run.status
            time.sleep(poll_interval)
    except Exception as e:
        raise Exception(f"Error waiting for run completion: {str(e)}")

def get_thread_messages(thread_id: str) -> List[Dict[str, Any]]:
    try:
        client = get_openai_client()
        response = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        return [
            {
                "id": msg.id,
                "role": msg.role,
                "content": [
                    {
                        "type": content.type,
                        "text": content.text.value if content.type == "text" else None
                    }
                    for content in msg.content
                ],
                "created_at": msg.created_at
            }
            for msg in response.data
        ]
    except Exception as e:
        raise Exception(f"Error getting thread messages: {str(e)}")

def delete_assistant(assistant_id: str) -> bool:
    try:
        client = get_openai_client()
        response = client.beta.assistants.delete(assistant_id=assistant_id)
        return response.deleted
    except Exception as e:
        raise Exception(f"Error deleting assistant: {str(e)}")

def delete_thread(thread_id: str) -> bool:
    try:
        client = get_openai_client()
        response = client.beta.threads.delete(thread_id=thread_id)
        return response.deleted
    except Exception as e:
        raise Exception(f"Error deleting thread: {str(e)}")