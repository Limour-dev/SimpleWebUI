import os
root = os.path.split(os.path.abspath(__file__))[0]

html = r'''
<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="">
  <script src=""></script>
</head>
<body>{content}</body>
</html>
'''.strip()

with open(os.path.join(root, 'assets', 'css', 'milligram.min.css'), 'r', encoding='utf-8') as rf:
    milligram = rf.read()

with open(os.path.join(root, 'assets', 'js', 'vue.min.js'), 'r', encoding='utf-8') as rf:
    vue = rf.read()
