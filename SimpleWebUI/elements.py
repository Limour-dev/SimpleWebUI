from winreg import QueryInfoKey

seed_id = 0
def random_id():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    global seed_id
    seed_id += 1
    result = '_'
    num = seed_id
    while num > 0:
        result += chars[num % 52]
        num //= 52
    return result

class Element:
    type = 'div'
    op = None
    root = None
    def __init__(self, content=None, id=None):
        self.contents = []
        self._id = id if id else random_id()
        self.attributes = {}
        if content is None:
            return
        self.contents.append(content)

    def append(self, el):
        el.root = self.root
        if self.op:
            self.op[-1].contents.append(el)
        else:
            self.contents.append(el)
        self.root.ids[el._id] = el

    @property
    def did(self):
        return 'd' + self._id

    def label(self, text='', *args, **kwargs):
        res = Label(*args, **kwargs)
        self.root.data[res.did] = text
        self.append(res)
        return res

    def button(self, text='', *args, **kwargs):
        res = Button(*args, **kwargs)
        self.root.data[res.did] = text
        self.append(res)
        return res

    def pinput(self, text='', *args, **kwargs):
        res = PInput(*args, **kwargs)
        self.root.vals[res.did] = text
        self.append(res)
        return res

    def link(self, text='', target='', *args, **kwargs):
        res = Link(*args, **kwargs)
        self.root.data[res.did] = text
        self.root.data[res.did + '_h'] = target
        self.append(res)
        return res

    def column(self, *args, **kwargs):
        res = Column(*args, **kwargs)
        self.append(res)
        return res

    def row(self, *args, **kwargs):
        res = Row(*args, **kwargs)
        self.append(res)
        return res

    def innerHTML(self):
        return ''.join(el.outerHTML() for el in self.contents)

    def outerHTML(self):
        if self.attributes:
            return r'<{type} {attributes}>{content}</{type}>'.format(
                type=self.type,
                attributes=' '.join(f'{k}="{v}"' for k, v in self.attributes.items()),
                content=self.innerHTML()
            )
        else:
            return r'<{type}>{content}</{type}>'.format(
                type=self.type,
                content=self.innerHTML()
            )

    def classes(self, classes):
        if 'class' in self.attributes:
            self.attributes['class'] += f' {classes}'
        else:
            self.attributes['class'] = classes
        return self
    def __enter__(self):
        if self.root.op:
            self.root.op.append(self)
        else:
            self.root.op = [self]
    def __exit__(self, exc_type, exc_val, exc_tb):
        if len(self.root.op) > 1:
            self.root.op.pop()
        else:
            self.root.op = None
    @property
    def v(self):
        did = self.did
        if did in self.root.delta:
            return self.root.delta[did]
        elif did in self.root.vals:
            return self.root.vals[did]
        else:
            return self.root.data[self.did]
    @v.setter
    def v(self, text=''):
        self.root.delta[self.did] = text

class Label(Element):
    type = 'label'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attributes['v-text'] = self.did

class Column(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classes('vertical')

class Row(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classes('horizontal')

async def btnClick(ui, el):
    print(el._id, 'clicked')

class Button(Element):
    type = 'button'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attributes['v-text'] = self.did
        self.attributes['@click'] = f"srpc.click('{self._id}')"
        self.click = btnClick

class PInput(Element):
    type = 'input'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attributes['v-model'] = self.did

class Link(Element):
    type = 'a'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attributes['v-text'] = self.did
        self.attributes[':href'] = self.did + '_h'
        self.attributes['target'] = "_blank"
