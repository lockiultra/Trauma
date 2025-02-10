// Обработчики событий для кнопки отправки и клавиши Enter (с поддержкой Shift+Enter для переноса строки)
document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("chat-input").addEventListener("keypress", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Функция отправки сообщения
function sendMessage() {
    const inputField = document.getElementById("chat-input");
    const messageText = inputField.value.trim();
    if (!messageText) return;
    addMessage("user", messageText);
    inputField.value = "";

    // Добавляем элемент загрузки для ответа бота
    const loadingElement = addLoadingMessage();

    // Отправляем POST-запрос на backend (URL /query)
    fetch("/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: messageText }),
    })
        .then((response) => {
        if (!response.ok) {
            throw new Error("Ошибка сервера");
        }
        return response.json();
    })
        .then((data) => {
        removeLoadingMessage(loadingElement);
        addMessage("bot", data.answer);
    })
        .catch((error) => {
        removeLoadingMessage(loadingElement);
        addMessage("bot", "Произошла ошибка при получении ответа.");
        console.error("Error:", error);
    });
}

// Функция добавления сообщения в чат
function addMessage(sender, text) {
    const chatMessages = document.getElementById("chat-messages");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);

    const bubbleDiv = document.createElement("div");
    bubbleDiv.classList.add("bubble");
    bubbleDiv.textContent = text;

    messageDiv.appendChild(bubbleDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Функция добавления элемента загрузки (анимации)
function addLoadingMessage() {
    const chatMessages = document.getElementById("chat-messages");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", "bot");

    const bubbleDiv = document.createElement("div");
    bubbleDiv.classList.add("bubble");

    const spinner = document.createElement("div");
    spinner.classList.add("loading-spinner");
    bubbleDiv.appendChild(spinner);

    messageDiv.appendChild(bubbleDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return messageDiv;
}

// Функция удаления элемента загрузки
function removeLoadingMessage(loadingElement) {
    loadingElement.remove();
}
