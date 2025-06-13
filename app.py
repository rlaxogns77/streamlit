import re
from openai import AsyncOpenAI, OpenAI

OPENAI_API_KEY = ""

client = AsyncOpenAI(
    api_key="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"
)

sync_client = OpenAI(
    api_key="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"
)


def llm_call(prompt: str,  model: str = "gpt-4o-mini") -> str:
    messages = []
    messages.append({"role": "user", "content": prompt})
    chat_completion = sync_client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return chat_completion.choices[0].message.content


async def llm_call_async(prompt: str,  model: str = "gpt-4o-mini") -> str:
    messages = []
    messages.append({"role": "user", "content": prompt})
    chat_completion = await client.chat.completions.create(
        model=model,
        messages=messages,
    )
    print(model,"완료")
    
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    test = llm_call("안녕")
    print(test)
