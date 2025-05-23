import random
import httpx
from mcp.server import FastMCP
import asyncio

app = FastMCP("web_search")

# @app.tool()
# async def random_number(min: int, max: int) -> int:
#     return random.randint(min, max)

# @app.tool()
# async def web_search_pro(query: str, num_results: int = 5) -> str:
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             'https://open.bigmodel.cn/api/paas/v4/tools',
#             headers={'Authorization': 'd4b8a475dcf0147ad0e8c108163f91d7.NLkUzxufYxKgOi2H'},
#             json={
#                 'tool': 'web-search-pro',
#                 'messages': [
#                     {'role': 'user', 'content': query}
#                 ],
#                 'stream': False,
#                 'num_results': num_results
#             }
#         )
#         return response.json()

@app.tool()
async def web_search(query: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://open.bigmodel.cn/api/paas/v4/tools',
            headers={'Authorization': 'd4b8a475dcf0147ad0e8c108163f91d7.NLkUzxufYxKgOi2H'},
            json={
                'tool': 'web-search',
                'messages': [
                    {'role': 'user', 'content': query}
                ],
                'stream': False
            }
        )
        print("1234567890--------")
        res_data = []
        for choice in response.json()['choices']:
            for message in choice['message']['tool_calls']:
                search_results = message.get('search_result')
                if not search_results:
                    continue
                for result in search_results:
                    # 将字典转换为字符串
                    if isinstance(result, dict):
                        result_str = f"标题: {result.get('title', '')}\n链接: {result.get('link', '')}\n摘要: {result.get('content', '')}"
                        res_data.append(result_str)
                    else:
                        res_data.append(str(result))
        return '\n\n\n'.join(res_data)
    
    
async def main():
    # 调用异步函数并获取返回值
    result = await web_search('你好用英文怎么说？')
    print(result)
    
if __name__ == "__main__":
    # 使用 asyncio 运行异步函数
    # asyncio.run(main())
    app.run(transport='stdio')