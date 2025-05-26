class Element:
    type = 'div'
    def __init__(self, content=None):
        self.contents = []
        self.attributes = {}
        if content is None:
            return
        self.contents.append(content)

    def label(self, content=None):
        res = Label(content)
        self.contents.append(res)
        return res

    def innerHTML(self):
        contents = (
            (el if (type(el) is str) else el.outerHTML()) for el in self.contents
        )
        return ''.join(contents)

    def outerHTML(self):
        attributes = ''
        return r'<{type}{attributes}>{content}</{type}>'.format(
            type = self.type,
            attributes = attributes,
            content = self.innerHTML()
        )

class Label(Element):
    type = 'label'