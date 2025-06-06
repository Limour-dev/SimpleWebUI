from aiohttp import web
from . import template as tp
from .elements import *
import aiohttp, json, traceback, asyncio

def j2s(obj):
    return json.dumps(obj, ensure_ascii=False)

class UI(Element):
    type = 'body'
    data = {}
    vals = {}
    ids = {}
    delta = {}
    def __init__(self):
        super().__init__()
        self.root = self
        self.prefix = '/'
        self.lang = 'zh-CN'
        self.title = 'SimpleWebUI'
        self.web = web
        self.app = web.Application(client_max_size=20 * 1024 ** 2)
        self.connected = set()
        self.srpc = {'click': self.click}

    async def click(self, _id):
        el = self.ids[_id]
        return await el.click(self, el)

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
        script = tp.script.replace('limour_ws_path', f'{self.prefix}ws')
        script = script.replace('limour_vue_methods', tp.methods)
        async def index(request):
            return web.Response(text=tp.html.format(
                lang = self.lang,
                title = self.title,
                vue=f'{self.prefix}vue.js',
                milligram = f'{self.prefix}milligram.css',
                content = self.innerHTML(),
                script = script.replace('limour_vue_vals', j2s(self.vals))\
                    .replace('limour_vue_data', j2s(self.data))
            ), content_type='text/html')
        self.app.router.add_get(f'{self.prefix}'.rstrip('/'), index)
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
                            if data['T'].startswith('upd'):
                                self.vals.update(data['D'])
                                await self.ws_update(data['D'])
                            if data['T'].endswith('rpc'):
                                try:
                                    res = await self.srpc['.'.join(data['N'])](*data['A'])
                                    if self.delta:
                                        D = await self.commit(False)
                                        await ws.send_str(j2s({
                                            'T': 'updrcr',
                                            'id': data['id'],
                                            'R': res,
                                            'D': D
                                        }))
                                        await self.ws_update(D, ws)
                                    else:
                                        await ws.send_str(j2s({
                                            'T': 'rcr',
                                            'id': data['id'],
                                            'R': res
                                        }))
                                except:
                                    await ws.send_str(j2s({
                                        'T': 'rcr',
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
    async def ws_send(self, text, ex=None):
        return await asyncio.gather(*(ws.send_str(text) for ws in self.connected if ws is not ex))
    async def notify(self, text):
        return await self.ws_send(j2s({
            'T': 'rpc',
            'N': 'alert',
            'A': [text]
        }))
    async def ws_update(self, data, ex=None):
        return await self.ws_send(j2s({
            'T': 'upd',
            'D': data
        }), ex=ex)
    def __getattr__(self, name) -> Element:
        return self.ids[name]
    async def commit(self, flag_s=True):
        if not self.delta:
            return
        for k,v in self.delta.items():
            if k in self.data:
                self.data[k] = v
            elif k in self.vals:
                self.vals[k] = v
            else:
                print(k, v, 'not found')
        if flag_s:
            await self.ws_update(self.delta)
        res = self.delta
        self.delta = {}
        return res
