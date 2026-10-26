

class WorkflowAgentState():
    """LangGraph 工作流在各节点之间流转的共享状态（State）。

    约定：
    - 每个字段都应当是“可序列化/可日志化”的简单类型或其组合。
    - 字段由不同节点逐步补全；未生成/未执行前通常为空字符串、空列表或 False。
    """

    # 用户原始输入（选题/要求/关键词等），作为整个工作流的源信息
    user_input: str

    # 生成的头条号文章标题（用于后台发布表单的“标题”）
    toutiao_title: str

    # 生成的头条号正文（纯文本/富文本源内容，后续可转 markdown 或直接发布）
    toutiao_content: str

    # 发布站点/渠道标识（例如：头条号后台域名或渠道名，用于路由/日志）
    toutiao_site: str

    # 是否需要“生成图片或抓取图片”的开关（图片节点据此决定是否执行）
    is_generate_image_or_crawl_image: bool

    # 文章配图本地路径列表（绝对/相对路径均可，但需可被上传节点读取）
    toutiao_image_path_list: list[str]

    # 生成过程提示信息/注意事项（给后续节点或最终输出用的说明性文本）
    toutiao_tip: str

    # 是否满足发布前置条件（标题/正文/图片等是否齐全，发布节点据此决定是否发布）
    is_can_publish_toutiao: bool

    # 文章 markdown 版本（用于预览/存档/发布节点需要 markdown 时使用）
    toutiao_markdown: str

    # 发布结果标记（发布节点执行后写入：成功 True，失败 False）
    is_publish_success: bool

    # 对外最终输出（总结/发布结果/链接/错误原因等，通常是工作流的最终返回文本）
    output: str