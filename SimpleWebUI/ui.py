from aiohttp import web
from . import template as tp

class Element:

    def __init__(self, content=None):
        self.contents = []
        if content is None:
            return
        elif type(content) is str:
            pass

    def label(self, content=None):
        res = Label(content)
        self.contents.append(res)
        return res


class Label(Element):
    def __init__(self, content=None):
        super().__init__(content)


class UI(Element):
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
        content = 'Hello World!'
        async def index(request):
            return web.Response(text=tp.html.format(
                lang = self.lang,
                title = self.title,
                content = content
            ), content_type='text/html')
        self.app.router.add_get(f'{self.prefix}', index)


