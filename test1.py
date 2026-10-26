from dotenv import load_dotenv
from common.llm import my_llm
from common.path_utils import get_file_path
load_dotenv(get_file_path('.env'),True)
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """查询指定城市的模拟天气数据。

    Args:
        city: 城市名称，例如杭州、北京、上海。
    """
    weather_data = {
        "杭州": "晴，25°C，湿度60%",
        "北京": "多云，18°C，湿度45%",
        "上海": "小雨，22°C，湿度80%",
    }

    return weather_data.get(
        city,
        f"没有找到{city}的模拟天气数据"
    )
    

agent = create_agent(
    model=my_llm,
    tools=[get_weather],
)

result = agent.invoke({"messages": [{"role": "user", "content": "武汉的天气如何"}]})
print(result["messages"][-1].content)
