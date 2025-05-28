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
<body><div id='app' style="display: flex;justify-content: center;">{content}</div>{script}</body>
</html>
'''.strip()

with open(os.path.join(root, 'assets', 'css', 'milligram.min.css'), 'r', encoding='utf-8') as rf:
    milligram = rf.read()

with open(os.path.join(root, 'assets', 'js', 'vue.min.js'), 'r', encoding='utf-8') as rf:
    vue = rf.read()

script = r'''
<script>
document.ws = new WebSocket("limour_ws_path");
let ws = document.ws;
ws.addEventListener('message', function(event) {
    if (event.data === "pong") {
        console.log("pong");
    } else {
        console.log("收到消息:", event.data);
    }
});
function sendHeartbeat() {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send("ping");
    }
}
document.ws_heartbeatTimer = setInterval(sendHeartbeat, 10000);

function getFunctionByPath(path) {
    return path.split('.').reduce((obj, key) => obj && obj[key], window);
}
function diffObject(a, b) {
  let c = {};
  Object.keys(b).forEach(key => {
    if (b[key] !== a[key]) {
      c[key] = a[key];
    }
  });
  return c;
}

const SRPC = () => {
  let reqId = 1;
  const pending = {};
  if (!document.ws.srpcListenerInstalled) {
    document.ws.addEventListener('message', e => {
      try {
        const msg = JSON.parse(e.data);
        if (msg && msg.__SRPC && pending[msg.id]) {
          if ('R' in msg) pending[msg.id].resolve(msg.R)
          else pending[msg.id].reject(msg.E)
          delete pending[msg.id];
        } else if (msg && msg.T === "rpc") {
          const fn = getFunctionByPath(msg.N);
          fn(...msg.A);
        } else if (msg && msg.T === "upd") {
          Object.assign(app, msg.D);
          Object.keys(vue_v).forEach(key => {
              if (msg.D.hasOwnProperty(key)) {
                vue_v[key] = msg.D[key];
              }
          });
        }
      } catch (e) { /* ignore */ }
    })
    document.ws.srpcListenerInstalled = true;
  }
  const getFunction = N => ((...A) => {
    return new Promise((resolve, reject) => {
      const id = reqId++;
      pending[id] = { resolve, reject };
      const msg = { T: "rpc", id, N, A };
      document.ws.send(JSON.stringify(msg));
    })
  })
  const proxyGet = (target, key) => {
    const N = target.N || [], newN = [...N, key], f = getFunction(newN);
    f.N = newN;
    return new Proxy(f, { get: proxyGet });
  }
  return new Proxy(() => {}, { get: proxyGet });
}
window.srpc = SRPC();
let vue_d = limour_vue_data;
window.vue_v = limour_vue_vals;
Object.assign(vue_d, vue_v);
window.app = new Vue({
el: '#app',
data: vue_d,
methods: limour_vue_methods,
});
window.ws_update = () => {
    let D = diffObject(app, vue_v);
    if (Object.keys(D).length > 0){
        document.ws.send(JSON.stringify({ T: "upd", D }));
    }
    return D;
}
</script>
'''.strip()

methods = '''
{
}
'''.strip()