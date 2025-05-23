import asyncio

from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
# 客户端
from mcp.shared.memory import (
    create_connected_server_and_client_session as create_session
)
# 这里需要引入服务端的 app 对象
from file_server import app


# 为 stdio 连接创建服务器参数
server_params = StdioServerParameters(
    # 服务器执行的命令，这里我们使用 uv 来运行 web_search.py
    command='uv',
    # 运行的参数
    args=['run', '--with', 'mcp', 'mcp', 'run', 'file_server.py'],
    # 环境变量，默认为 None，表示使用当前环境变量
    # env=None
)


async def sampling_callback(context, params):
    print("---------sampling_callback---------")
    print(context)
    print(params)
    
    # # 创建 stdio 客户端
    # async with stdio_client(server_params) as (stdio, write):
    #     # 创建 ClientSession 对象
    #     async with ClientSession(stdio, write) as session:
    #         # 初始化 ClientSession
    #         await session.initialize()

    #         # 列出可用的工具
    #         response = await session.list_tools()
    #         print("---------list_tools---------")
    #         print(response)

    #         print("---------context---------")
    #         print(context)
    #         print("---------params---------")
    #         print(params)
    #         # 调用工具
    #         response = await session.call_tool(context, params)
    #         print("---------call_tool---------")
    #         print(response)


# if __name__ == '__main__':
#     asyncio.run(main())

async def main():
    async with create_session(
        app._mcp_server,
        # sampling_callback=sampling_callback
    ) as client_session:
        print("---------client_session---------")
        await client_session.call_tool(
            name='delete_file', 
            arguments={'file_path': '/Users/sam/Desktop/WechatIMG3875.jpg'}
        )

if __name__ == '__main__':
    asyncio.run(main())
