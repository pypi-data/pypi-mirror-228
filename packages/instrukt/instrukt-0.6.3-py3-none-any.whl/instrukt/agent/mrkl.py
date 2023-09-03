import re
from typing import (
    Optional,
    Tuple,
)

from langchain.agents.mrkl.base import FINAL_ANSWER_ACTION, ZeroShotAgent


class ZeroShotInstruktAgent(ZeroShotAgent):

    def _extract_tool_and_input(self, text: str) -> Optional[Tuple[str, str]]:
        return get_action_and_input(text)


#HACK: shell parsing
def get_action_and_input(llm_output: str) -> Tuple[str, str]:
    """Parse out the action and input from the LLM output."""
    if FINAL_ANSWER_ACTION in llm_output:
        return "Final Answer", llm_output.split(
            FINAL_ANSWER_ACTION)[-1].strip()
    regex = r"Action: (.*?)[\n]*Action Input:\n```\n(.*)\n```"

    match = re.search(regex, llm_output, re.DOTALL)
    if not match:
        return "Final Answer", llm_output
        # raise ValueError(f"Could not parse LLM output: `{llm_output}`")
    action = match.group(1).strip()
    action_input = match.group(2)
    # print(f"[b]Action Input:[/]\n{action_input}")

    return action, action_input.strip(" ").strip('"')
