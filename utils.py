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
