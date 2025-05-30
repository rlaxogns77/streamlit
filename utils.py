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
