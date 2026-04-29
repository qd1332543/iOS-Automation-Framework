import re
from pathlib import Path
from tools.webui.config import PROJECT_ROOT, AI_PROVIDER, AI_API_KEY, AI_MODEL
from tools.webui.services.file_service import get_file_content

# 关键词 -> 相关文件映射
_KEYWORD_FILES = {
    "登录": ["UI_Automation/Pages/login_page.py", "API_Automation/cases/test_user.py"],
    "login": ["UI_Automation/Pages/login_page.py", "API_Automation/cases/test_user.py"],
    "购物车": ["UI_Automation/Pages/cart_page.py", "API_Automation/cases/test_cart.py"],
    "cart": ["UI_Automation/Pages/cart_page.py", "API_Automation/cases/test_cart.py"],
    "订单": ["API_Automation/api/order_api.py", "API_Automation/cases/test_order.py"],
    "order": ["API_Automation/api/order_api.py", "API_Automation/cases/test_order.py"],
    "page object": ["UI_Automation/Pages/base_page.py"],
    "配置": ["config/environments.yaml", "pytest.ini"],
    "config": ["config/environments.yaml", "pytest.ini"],
    "allure": ["conftest.py", "pytest.ini"],
    "并发": ["pytest.ini"],
    "appium": ["UI_Automation/Pages/base_page.py"],
}

_DEFAULT_FILES = ["README.md", "pytest.ini", "conftest.py"]


def _retrieve_context(question: str) -> list[dict]:
    """根据问题关键词检索相关文件片段"""
    q = question.lower()
    files = list(_DEFAULT_FILES)
    for kw, paths in _KEYWORD_FILES.items():
        if kw in q:
            files.extend(paths)

    # 去重，最多取 6 个
    seen = set()
    unique = []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    unique = unique[:6]

    snippets = []
    for path in unique:
        result = get_file_content(path)
        if "content" in result:
            content = result["content"]
            # 截取前 150 行
            lines = content.splitlines()[:150]
            snippets.append({"path": path, "content": "\n".join(lines)})
    return snippets


def _mock_answer(question: str, snippets: list[dict]) -> str:
    refs = "\n".join(f"- `{s['path']}`" for s in snippets)
    return (
        f"（Mock 模式）基于以下文件检索到相关内容：\n{refs}\n\n"
        f"请配置 `AI_PROVIDER=claude` 和 `AI_API_KEY` 以获得真实 AI 回答。\n\n"
        f"你的问题：{question}"
    )


async def _claude_answer(question: str, snippets: list[dict]) -> str:
    try:
        import anthropic
    except ImportError:
        return "请先安装 anthropic 包：pip install anthropic"

    context = "\n\n".join(
        f"# {s['path']}\n```\n{s['content']}\n```" for s in snippets
    )
    system = (
        "你是 iOS-Automation-Framework 的项目助手。"
        "只能基于提供的项目上下文回答。"
        "如果上下文不足，说明不确定并建议用户查看哪些文件。"
        "回答涉及命令时，只推荐项目中已有的安全命令。"
        "不要输出密钥、token、证书、密码。"
        "如果用户询问 UI 自动化运行环境，说明 iOS UI 自动化依赖 macOS + Xcode + Appium。"
    )

    client = anthropic.Anthropic(api_key=AI_API_KEY)
    message = client.messages.create(
        model=AI_MODEL,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": f"项目上下文：\n{context}\n\n问题：{question}"}],
    )
    return message.content[0].text


async def answer(question: str) -> dict:
    snippets = _retrieve_context(question)
    if AI_PROVIDER == "claude" and AI_API_KEY:
        text = await _claude_answer(question, snippets)
    else:
        text = _mock_answer(question, snippets)
    return {
        "answer": text,
        "references": [s["path"] for s in snippets],
    }
