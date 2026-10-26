import asyncio

from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser

from __001__langgraph_workflow.workflow_agent_state import WorkflowAgentState
from common.llm import my_llm


class ToutiaoTravelOutput(BaseModel):
    title: str = Field(description="头条号图文的标题，建议不超过30个中文字符，信息明确有吸引力")
    content: str = Field(description="头条号正文，不超过800个中英文字符，适合资讯/攻略阅读，段落清晰")
    site: str = Field(description="从用户输入中提取的地点：城市/省份/国家/景区/山脉/河流等；无法提取则返回空字符串")


async def generate_toutiao_travel_post(user_input: str):
    parser = JsonOutputParser(pydantic_object=ToutiaoTravelOutput)
    format_instructions = parser.get_format_instructions()

    messages = [
        SystemMessage(content=(
            "你是一个为【今日头条 / 头条号】撰写【旅行图文】稿件的文案助手。\n"
            "请根据用户提供的主题或地点，生成适合头条号发布的旅行类内容，要求包含：\n"
            "1. 标题（title）：点题清晰，建议不超过30个中文字符\n"
            "2. 正文（content）：有攻略感与可读性，可含目的地亮点、行程建议、注意事项、个人体验等，"
            "语气自然，适合信息流阅读\n"
            "3. 地点（site）：从用户输入中提取一个城市/省份/国家/景区/山脉/河流等关键词\n"
            "请你严格按照以下格式返回结果：\n"
            f"{format_instructions}"
        )),
        HumanMessage(content=user_input)
    ]
    final_answer = ""
    for chunk in my_llm.stream(messages):
        print(chunk.content, end="", flush=True)
        final_answer += chunk.content
    out = parser.parse(final_answer)
    return out.get("title", ""), out.get("content", ""), out.get("site", "")


async def text_generate_node(state: WorkflowAgentState):
    print("开始生成头条号旅行标题和正文")
    user_input = state.get("user_input", "")
    title, content, site = await generate_toutiao_travel_post(user_input)

    state['toutiao_title'] = title
    state['toutiao_content'] = content
    state['toutiao_site'] = site
    print("完成生成头条号旅行标题和正文")
    return state


if __name__ == '__main__':
    result = asyncio.run(text_generate_node({"user_input": "山东泰安泰山两日游"}))
    print(result)
    