from aiohttp import web
from . import template as tp
from .elements import *
import aiohttp, json, traceback

class UI(Element):
    type = 'body'
    def __init__(self):
        super().__init__()
        self.prefix = '/'
        self.lang = 'zh-CN'
        self.title = 'SimpleWebUI'
        self.web = web
        self.app = web.Application(client_max_size=20 * 1024 ** 2)
        self.connected = set()
        self.srpc = {'min': min}

    async def run_app(self, host='0.0.0.0', port=8118):
        self.setup()
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, host=host, port=port)
        return await site.start()

    def run(self, host='0.0.0.0', port=8118):
        self.setup()
        return web.run_app(self.app, host=host, port=port)

    def setup(self):
        async def js(request):
            return web.Response(
                text=tp.vue,
                content_type='application/javascript'
            )
        self.app.router.add_get(f'{self.prefix}vue.js', js)
        async def css(request):
            return web.Response(
                text=tp.milligram,
                content_type='text/css'
            )
        self.app.router.add_get(f'{self.prefix}milligram.css', css)
        async def index(request):
            return web.Response(text=tp.html.format(
                lang = self.lang,
                title = self.title,
                vue=f'{self.prefix}vue.js',
                milligram = f'{self.prefix}milligram.css',
                content = self.innerHTML(),
                script = tp.script.replace('limour_ws_path', f'{self.prefix}ws')
            ), content_type='text/html')
        self.app.router.add_get(f'{self.prefix}', index)
        self.heartbeat()

    def heartbeat(self):
        async def websocket_handler(request):
            ws = web.WebSocketResponse()
            await ws.prepare(request)
            self.connected.add(ws)
            print('Browser connected')

            try:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        if msg.data == 'ping':
                            await ws.send_str('pong')
                            continue
                        print(f"收到浏览器消息: {msg.data}")
                        try:
                            data = json.loads(msg.data)
                            if data['type'] == 'srpc':
                                try:
                                    res = self.srpc['.'.join(data['N'])](*data['A'])
                                    await ws.send_str(json.dumps({
                                        '__SRPC': True,
                                        'id': data['id'],
                                        'R': res
                                    }))
                                except:
                                    await ws.send_str(json.dumps({
                                        '__SRPC': True,
                                        'id': data['id'],
                                        'E': traceback.format_exc()
                                    }))
                        except:
                            traceback.print_exc()
                        # await ws.send_str(f"服务器收到: {msg.data}")
            finally:
                self.connected.remove(ws)
                print('Browser disconnected')
            return ws
        self.app.router.add_get(f'{self.prefix}ws', websocket_handler)

