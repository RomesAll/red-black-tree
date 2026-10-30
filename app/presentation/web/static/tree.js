const container = document.getElementById('network');
const status = document.getElementById('ws-status');
let network = null;

// Проверяем, есть ли в URL параметр stream=true
const urlParams = new URLSearchParams(window.location.search);
const isStreamMode = urlParams.get('stream') === 'true';

// Таймер для Debounce (чтобы не спамить GET-запросами при стриминге)
let renderTimeout = null;

// --- 1. Загрузка дерева через HTTP (используется только для обычного режима) ---
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

// --- 2. Отрисовка графа (Vis.js) ---
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

        // Формируем узел
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

        // Формируем связи
        if (parentId !== null) {
            edges.push({
                from: parentId,
                to: id,
                arrows: { to: { enabled: true, scaleFactor: 0.8 } },
                color: { color: '#9ca3af', highlight: '#3b82f6' },
                width: 2,
                smooth: { type: 'cubicBezier', forceDirection: 'vertical', roundness: 0.4 }
            });
        }

        traverse(node.left, id);
        traverse(node.right, id);
    }

    traverse(rootNode);

    const data = {
        nodes: new vis.DataSet(nodes),
        edges: new vis.DataSet(edges)
    };

    const options = {
        layout: {
            hierarchical: {
                direction: 'UD',
                sortMethod: 'directed',
                levelSeparation: 90,
                nodeSpacing: 80
            }
        },
        physics: false,
        interaction: { zoomView: true, dragView: true, hover: true }
    };

    if (network) {
        network.setData(data);
    } else {
        container.innerHTML = '';
        network = new vis.Network(container, data, options);
    }
}

// --- 3. Подключение к WebSocket ---
function connectWS() {
    // Если это стриминг, идем на /stream, иначе на обычный сокет
    const wsUrl = isStreamMode
        ? `ws://${window.location.host}/ws/trees/stream`
        : `ws://${window.location.host}/ws/trees/${treeId}`;

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        status.innerText = isStreamMode ? "WebSocket: Стриминг..." : "WebSocket: Подключен";
        status.style.background = "rgba(46, 204, 113, 0.9)";

        // Если стриминг, сразу отправляем данные и ID
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

        if (isStreamMode) {
            // Когда стриминг завершается (сервер закрывает сокет),
            // перезагружаем страницу уже в обычном режиме (убираем ?stream=true)
            const newUrl = window.location.pathname;
            window.history.replaceState({}, '', newUrl);
            window.location.reload();
        } else {
            // Обычное переподключение
            setTimeout(connectWS, 3000);
        }
    };

    ws.onmessage = (e) => {
        const msg = JSON.parse(e.data);
        console.log("Событие из WS:", msg);

        // --- ОБРАБОТКА СНИМКА ДЕРЕВА (СТРИМИНГ) ---
        if (msg.type === "TREE_UPDATE") {
            // Рисуем сразу, без GET-запроса
            drawGraph(msg.data);
            return;
        }

        // --- ОБРАБОТКА ОБЫЧНЫХ СОБЫТИЙ (вставка через HTTP) ---
        if (['NODE_INSERTED', 'NODE_DELETED', 'COLOR_CHANGED', 'ROTATE_LEFT', 'ROTATE_RIGHT'].includes(msg.type)) {
            // Debounce: ждем 150мс, если прилетит еще событие — сбрасываем таймер
            if (renderTimeout) clearTimeout(renderTimeout);
            renderTimeout = setTimeout(() => {
                loadTree();
            }, 150);
        }
    };
}

// --- 4. Обработка кнопок Добавить/Удалить ---
document.getElementById('add-node-btn').addEventListener('click', async () => {
    const keyInput = document.getElementById('node-key');
    const valueInput = document.getElementById('node-value');

    const key = parseInt(keyInput.value);
    const value = valueInput.value;
    if (isNaN(key)) return alert("Введите число для ключа");

    try {
        const res = await fetch(`/trees/${treeId}/nodes/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key, value })
        });

        if (!res.ok) {
            const error = await res.json();
            alert(error.message || "Ошибка вставки");
        } else {
            keyInput.value = '';
            valueInput.value = '';
        }
    } catch (e) {
        alert("Ошибка сети");
    }
});

document.getElementById('delete-node-btn').addEventListener('click', async () => {
    const keyInput = document.getElementById('node-key');
    const key = parseInt(keyInput.value);
    if (isNaN(key)) return alert("Введите число для ключа");

    try {
        const res = await fetch(`/trees/${treeId}/nodes/`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key })
        });

        if (!res.ok) {
            const error = await res.json();
            alert(error.message || "Ошибка удаления");
        } else {
            keyInput.value = '';
        }
    } catch (e) {
        alert("Ошибка сети");
    }
});

// --- 5. Поиск узла ---
document.getElementById('search-node-btn').addEventListener('click', () => {
    const keyToFind = parseInt(document.getElementById('search-node-input').value);
    if (isNaN(keyToFind)) return alert("Введите число");

    if (!network) return alert("Дерево пустое");

    // Сбрасываем цвета всех узлов
    const allNodes = network.body.data.nodes.get();
    const resetNodes = allNodes.map(n => {
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

    const targetNode = network.body.data.nodes.get(keyToFind);

    if (targetNode) {
        network.body.data.nodes.update({
            id: keyToFind,
            color: { background: '#f59e0b', border: '#b45309' }
        });

        network.focus(keyToFind, {
            scale: 1.2,
            animation: { duration: 500, easingFunction: "easeInOutQuad" }
        });
    } else {
        alert(`Узел с ключом ${keyToFind} не найден.`);
    }
});

document.getElementById('search-node-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') document.getElementById('search-node-btn').click();
});


// --- ИНИЦИАЛИЗАЦИЯ ---
loadTree();
connectWS();