const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");

let userMessage = "Can I change my appointment time online?";
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", `${className}`);
  let chatContent = className === "outgoing" ? `<p>${message}</p>`: `<img src="icon.png" style="height: 40px;"><p>${message}</p>`;
  chatLi.innerHTML = chatContent;
  chatLi.querySelector("p").textContent = message;
  return chatLi;
}

const generateResponse = (chatElement) => {
  const API_URL = "http://localhost:5000/chat";
  const messageElement = chatElement.querySelector("p");
  
  const requestOptions = {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({
          message: userMessage
      })
  };

  fetch(API_URL, requestOptions)
      .then(res => res.json())
      .then(data => {
          const responseMessage = data.response;
          simulateTyping(messageElement, responseMessage);
      })
      .catch(() => {
          messageElement.classList.add("error");
          messageElement.textContent = "Oops! Something went wrong. Please try again.";
      })
      .finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
}

const simulateTyping = (element, message) => {
  const typingIndicator = document.createElement('div');
  // typingIndicator.classList.add('typing-indicator');
  // typingIndicator.textContent = "Typing...";
  chatbox.appendChild(typingIndicator);
  
  let index = 0;
  element.textContent = ''; 
  const typingEffect = setInterval(() => {
      if (index < message.length) {
          element.textContent += message.charAt(index);
          index++;
      } else {
          clearInterval(typingEffect);
          chatbox.removeChild(typingIndicator); 
      }
  }, 10); 
}


const handleChat = () => {
  userMessage = chatInput.value.trim();
  if(!userMessage) return;

  chatInput.value = "";
  chatInput.style.height = `${inputInitHeight}px`;

  chatbox.appendChild(createChatLi(userMessage, "outgoing"));
  chatbox.scrollTo(0, chatbox.scrollHeight);

  setTimeout(() => {
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    generateResponse(incomingChatLi);
  }, 600);
}

chatInput.addEventListener("input", () => {
  chatInput.style.height = `${inputInitHeight}px`;
  chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
  if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
    e.preventDefault();
    handleChat();
  }
});

sendChatBtn.addEventListener("click", handleChat);
closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));