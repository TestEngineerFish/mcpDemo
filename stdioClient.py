# 客户端连接MCPServer的工具
import asyncio

from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from mcp.shared.context import RequestContext
from mcp.types import (
    TextContent,
    CreateMessageRequestParams,
    CreateMessageResult,
)

server_params = StdioServerParameters(
    command='uv',
    args=['run', '--with', 'mcp', 'mcp', 'run', 'web_search.py'],
)


async def sampling_callback(
        context: RequestContext[ClientSession, None],
        params: CreateMessageRequestParams,
):
    # 获取工具发送的消息并显示给用户
    input_message = input(params.messages[0].content.text)
    # 将用户输入发送回工具
    return CreateMessageResult(
        role='user',
        content=TextContent(
            type='text',
            text=input_message.strip().upper() or 'Y'
        ),
        model='user-input',
        stopReason='endTurn'
    )


async def main():
    # 创建 stdio 客户端
    async with stdio_client(server_params) as (stdio, write):
        # 创建 ClientSession 对象
        async with ClientSession(stdio, write) as session:
            # 初始化 ClientSession
            await session.initialize()
            # 列出可用的工具
            response = await session.list_tools()
            print(response)
            print("4、list_tools")
            response = await session.call_tool(
                'web_search',
                {'query': '你好用英文怎么说？'}
            )
            # 获取工具最后执行完的返回结果
            print(response)


if __name__ == '__main__':
    asyncio.run(main())

