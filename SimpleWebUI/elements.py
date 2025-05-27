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
        self.attributes = {'id': id if id else random_id()}
        if content is None:
            return
        self.contents.append(content)

    def append(self, el):
        el.root = self.root
        if self.op:
            self.op[-1].contents.append(el)
        else:
            self.contents.append(el)
        return el

    def label(self, *args, **kwargs):
        res = Label(*args, **kwargs)
        return self.append(res)

    def column(self, *args, **kwargs):
        res = Column(*args, **kwargs)
        return self.append(res)

    def row(self, *args, **kwargs):
        res = Row(*args, **kwargs)
        return self.append(res)

    def innerHTML(self):
        return ''.join((el if (type(el) is str) else el.outerHTML()) for el in self.contents)

    def outerHTML(self):
        return r'<{type} {attributes}>{content}</{type}>'.format(
            type = self.type,
            attributes = ' '.join(f'{k}="{v}"' for k,v in self.attributes.items()),
            content = self.innerHTML()
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

class Label(Element):
    type = 'label'

class Column(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classes('vertical')

class Row(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classes('horizontal')
