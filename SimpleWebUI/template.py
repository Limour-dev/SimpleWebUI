import os
root = os.path.split(os.path.abspath(__file__))[0]

html = r'''
<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="{milligram}">
  <script src="{vue}"></script>
</head>
<body>{content}{script}</body>
</html>
'''.strip()

with open(os.path.join(root, 'assets', 'css', 'milligram.min.css'), 'r', encoding='utf-8') as rf:
    milligram = rf.read()

with open(os.path.join(root, 'assets', 'js', 'vue.min.js'), 'r', encoding='utf-8') as rf:
    vue = rf.read()

script = r'''
<script>
document.ws = new WebSocket("limour_ws_path");
document.ws.onmessage = function(event) {
    if (event.data === "pong") {
        console.log("pong");
    } else {
        console.log("收到消息:", event.data);
    }
};
let ws = document.ws;
function sendHeartbeat() {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send("ping");
    }
}
document.ws_heartbeatTimer = setInterval(sendHeartbeat, 10000);
</script>
'''.strip()