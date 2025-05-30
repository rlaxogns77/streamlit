from typing import List
from utils import llm_call

def prompt_chain_workflow_2(initial_input: str, prompt_chain: List[str]) -> List[str]:
    response_chain = []
    response = initial_input

    for i, prompt in enumerate(prompt_chain, 1):
        print(f"\n==== 단계 {i} ====\n")
        final_prompt = f"{prompt}\n\n 사용자 입력: {initial_input} \n\n 문맥(Context):\n{response}"
        print(f" 프롬프트:\n{final_prompt}\n")

        response = llm_call(final_prompt)
        response_chain.append(response)
        print(f" 응답:\n{response}\n")

    return response_chain
