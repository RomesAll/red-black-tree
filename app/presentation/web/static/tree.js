const container = document.getElementById('network');
const status = document.getElementById('ws-status');
let network = null;

// Проверяем, есть ли в URL параметр stream=true
const urlParams = new URLSearchParams(window.location.search);
const isStreamMode = urlParams.get('stream') === 'true';

// --- 1. Загрузка и отрисовка ---
async function loadTree() {
    try {
        const res = await fetch(`/trees/${treeId}/`);
        if (!res.ok) throw new Error("Дерево не найдено");
        const data = await res.json();
        drawGraph(data.root);
    } catch (e) {
        container.innerHTML = `<h2 style="text-align:center;margin-top:10%;color:red">${e.message}</h2>`;
    }
}

function drawGraph(rootNode) {
    if (!rootNode) {
        container.innerHTML = "<h2 style='text-align:center;margin-top:10%'>Дерево пустое</h2>";
        if (network) { network.destroy(); network = null; }
        return;
    }

    const nodes = [];
    const edges = [];

    function traverse(node, parentId = null) {
        if (!node) return;
        const id = node.key;
        nodes.push({
            id: id,
            label: String(node.key),
            title: `Значение: ${node.value || 'пусто'}\nЦвет: ${node.color}`,
            color: {
                background: node.color === 'RED' ? '#ef4444' : '#1f2937',
                border: node.color === 'RED' ? '#b91c1c' : '#111827',
                highlight: { background: '#3b82f6', border: '#1d4ed8' }
            },
            font: { color: '#ffffff', size: 16, face: 'Arial', bold: true },
            shape: 'circle', size: 35, borderWidth: 3,
            shadow: { enabled: true, color: 'rgba(0,0,0,0.3)', size: 10, x: 2, y: 2 }
        });

        if (parentId !== null) {
            edges.push({ from: parentId, to: id, arrows: { to: { enabled: true, scaleFactor: 0.8 } }, color: { color: '#9ca3af', highlight: '#3b82f6' }, width: 2, smooth: { type: 'cubicBezier', forceDirection: 'vertical', roundness: 0.4 } });
        }
        traverse(node.left, id);
        traverse(node.right, id);
    }

    traverse(rootNode);
    const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
    const options = { layout: { hierarchical: { direction: 'UD', sortMethod: 'directed', levelSeparation: 90, nodeSpacing: 80 } }, physics: false, interaction: { zoomView: true, dragView: true, hover: true } };

    if (network) { network.setData(data); }
    else { container.innerHTML = ''; network = new vis.Network(container, data, options); }
}

// --- 2. WebSocket ---
function connectWS() {
    // Если это стриминг — идем на /stream, иначе на обычный прослушиватель
    const wsUrl = isStreamMode
        ? `ws://${window.location.host}/ws/trees/stream`
        : `ws://${window.location.host}/ws/trees/${treeId}`;

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        status.innerText = isStreamMode ? "WebSocket: Стриминг..." : "WebSocket: Подключен";
        status.style.background = "rgba(46, 204, 113, 0.9)";

        // Если это стриминг, сразу отправляем данные
        if (isStreamMode) {
            const streamData = localStorage.getItem('stream_data');
            if (streamData) {
                ws.send(JSON.stringify({
                    nodes: JSON.parse(streamData),
                    tree_id: treeId
                }));
                localStorage.removeItem('stream_data');
            }
        }
    };

    ws.onclose = () => {
        status.innerText = "WebSocket: Отключен";
        status.style.background = "rgba(231, 76, 60, 0.9)";

        // --- ВОТ ГЛАВНОЕ ИСПРАВЛЕНИЕ ---
        if (isStreamMode) {
            // Если стриминг закончился (сокет закрылся со стороны сервера),
            // переподключаемся уже в режиме ОБЫЧНОГО ПРОСЛУШИВАНИЯ.
            // Убираем флаг ?stream=true из URL, чтобы при перезагрузке страница не пыталась стримить снова
            const newUrl = window.location.pathname;
            window.history.replaceState({}, '', newUrl);

            // Меняем глобальный флаг и переподключаемся
            window.location.reload(); // Самый простой способ — перезагрузить страницу без ?stream=true
        } else {
            // Если это был обычный сокет, пробуем переподключиться через 3 секунды
            setTimeout(connectWS, 3000);
        }
    };

    ws.onmessage = (e) => {
        const msg = JSON.parse(e.data);
        console.log("WS:", msg);

        if (['NODE_INSERTED', 'NODE_DELETED', 'COLOR_CHANGED', 'ROTATE_LEFT', 'ROTATE_RIGHT'].includes(msg.type)) {
            setTimeout(loadTree, 100);
        }

        // Если пришел статус "Конец", сервер сейчас закроет сокет.
        // Мы можем ничего не делать, сработает onclose и перезагрузит страницу.
    };
}

// --- 3. Кнопки ---
document.getElementById('add-node-btn').addEventListener('click', async () => {
    const key = parseInt(document.getElementById('node-key').value);
    const value = document.getElementById('node-value').value;
    if (isNaN(key)) return alert("Введите число");

    const res = await fetch(`/trees/${treeId}/nodes/`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key, value })
    });
    if (!res.ok) alert("Ошибка вставки");
    else { document.getElementById('node-key').value = ''; document.getElementById('node-value').value = ''; }
});

document.getElementById('delete-node-btn').addEventListener('click', async () => {
    const key = parseInt(document.getElementById('node-key').value);
    if (isNaN(key)) return alert("Введите число");

    const res = await fetch(`/trees/${treeId}/nodes/`, {
        method: 'DELETE', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key })
    });
    if (!res.ok) alert("Ошибка удаления");
    else { document.getElementById('node-key').value = ''; }
});


// --- ПОИСК УЗЛА В ДЕРЕВЕ ---
document.getElementById('search-node-btn').addEventListener('click', () => {
    const keyToFind = parseInt(document.getElementById('search-node-input').value);
    if (isNaN(keyToFind)) return alert("Введите число");

    if (!network) return alert("Дерево пустое");

    // Сбрасываем цвета всех узлов обратно (на случай, если искали до этого)
    const allNodes = network.body.data.nodes.get();
    const resetNodes = allNodes.map(n => {
        // Возвращаем цвета в зависимости от того, красный узел или черный
        const isRed = n.title.includes('Цвет: RED');
        return {
            id: n.id,
            color: {
                background: isRed ? '#ef4444' : '#1f2937',
                border: isRed ? '#b91c1c' : '#111827',
            }
        };
    });
    network.body.data.nodes.update(resetNodes);

    // Ищем нужный узел (у нас ID узла на графе = его ключу)
    const targetNode = network.body.data.nodes.get(keyToFind);

    if (targetNode) {
        // Подсвечиваем его желтым/оранжевым
        network.body.data.nodes.update({
            id: keyToFind,
            color: {
                background: '#f59e0b', // Оранжевый
                border: '#b45309'
            }
        });

        // Плавно центрируем граф на этом узле
        network.focus(keyToFind, {
            scale: 1.2,
            animation: {
                duration: 500,
                easingFunction: "easeInOutQuad"
            }
        });
    } else {
        alert(`Узел с ключом ${keyToFind} не найден в этом дереве.`);
    }
});

// Поддержка поиска по нажатию Enter
document.getElementById('search-node-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('search-node-btn').click();
    }
});

// --- Инициализация ---
loadTree();
connectWS();