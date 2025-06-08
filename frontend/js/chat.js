let socket = null;

document.getElementById("connectBtn").addEventListener("click", () => {
    const chatId = document.getElementById("chatId").value;
    const chatBox = document.getElementById("chat");

    if (socket) {
        socket.close();
    }

    socket = new WebSocket(`ws://${window.location.hostname}:8000/ws/chat/${chatId}/`);

    socket.onopen = () => {
        chatBox.innerHTML += "<div><em>Connected.</em></div>";
    };

    socket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        chatBox.innerHTML += `<div><strong>${data.username}</strong>: ${data.message}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    socket.onclose = () => {
        chatBox.innerHTML += "<div><em>Disconnected.</em></div>";
    };
});

document.getElementById("sendBtn").addEventListener("click", () => {
    const input = document.getElementById("messageInput");
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ message: input.value }));
        input.value = "";
    }
});
