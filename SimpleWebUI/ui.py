from aiohttp import web
from . import template as tp
from .elements import *

class UI(Element):
    type = 'body'
    def __init__(self):
        super().__init__()
        self.prefix = '/'
        self.lang = 'zh-CN'
        self.title = 'SimpleWebUI'
        self.web = web
        self.app = web.Application(client_max_size=20 * 1024 ** 2)

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
                content = self.innerHTML()
            ), content_type='text/html')
        self.app.router.add_get(f'{self.prefix}', index)
