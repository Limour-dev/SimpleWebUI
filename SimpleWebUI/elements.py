seed_id = 0
def random_id():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    global seed_id
    seed_id += 1
    result = ''
    num = seed_id
    while num > 0:
        result += chars[num % 52]
        num //= 52
    return result

class Element:
    type = 'div'
    def __init__(self, content=None):
        self.contents = []
        self.attributes = {'id': random_id()}
        if content is None:
            return
        self.contents.append(content)

    def label(self, content=None):
        res = Label(content)
        self.contents.append(res)
        return res

    def innerHTML(self):
        return ''.join((el if (type(el) is str) else el.outerHTML()) for el in self.contents)

    def outerHTML(self):
        return r'<{type} {attributes}>{content}</{type}>'.format(
            type = self.type,
            attributes = ' '.join(f'{k}="{v}"' for k,v in self.attributes.items()),
            content = self.innerHTML()
        )

class Label(Element):
    type = 'label'