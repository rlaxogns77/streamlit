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
