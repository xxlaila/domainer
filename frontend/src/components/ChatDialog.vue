<template>
  <div class="chat-dialog">
    <div v-if="showBot" class="bot-icon" @click="toggleChat">
      <img src="./icons/IMG_202404037352_75x75.png" alt="Robot Icon">
    </div>
    <div v-if="showChat" class="chat-container">
      <div class="chat-header">
        <span>AI运维助手</span>
        <button class="close-btn" @click="toggleChat">X</button>
      </div>
      <div class="chat-messages" ref="messageContainer">
        <div v-for="(message, index) in messages" :key="index" class="message" :class="{ 'user-message': message.sender === 'user', 'bot-message': message.sender === 'bot' }">
          <div class="message-info">{{ message.sender }} {{ message.time }}</div>
          <br/>
          <div class="message-text" :class="{ 'user-text': message.sender === 'user', 'bot-text': message.sender === 'bot' }">{{ message.text }}</div>
        </div>
      </div>
        <input v-model="inputMessage" @keyup.enter="sendMessage" class="input-message" placeholder="Type your message...">
        <button class="send-btn" @click="sendMessage">Send</button> <!-- 新增的发送按钮 -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const showBot = ref(true);
const showChat = ref(false);
const inputMessage = ref('');
const messages = ref([]);

function toggleChat() {
  showChat.value = !showChat.value;
}

function sendMessage() {
  if (inputMessage.value.trim() !== '') {
    messages.value.push({
      sender: 'user',
      text: inputMessage.value,
      time: getCurrentTime()
    });
    // 发送消息到后端的 API，假设后端 API 是 /chat/message
    fetch(`${process.env.VUE_APP_BASE_API}/wechat/chat/message/`, {
      method: 'POST',
      body: JSON.stringify({ message: inputMessage.value }),
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include' // 或者 credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
      messages.value.push({
        sender: 'bot',
        text: data.data, // Assuming the bot's response is in data.data
        time: getCurrentTime()
      });
    })
    .catch(error => {
      console.error('Error:', error);
    });
    inputMessage.value = '';
    scrollToBottom();
  }
}

function getCurrentTime() {
  const now = new Date();
  const hours = now.getHours().toString().padStart(2, '0');
  const minutes = now.getMinutes().toString().padStart(2, '0');
  return `${hours}:${minutes}`;
}

function scrollToBottom() {
  const messageContainer = document.querySelector('.chat-messages');
  if (messageContainer) {
    messageContainer.scrollTop = messageContainer.scrollHeight;
  }
}

onMounted(() => {
  scrollToBottom();
});
</script>

<style scoped>
.chat-dialog {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999; /* 设置一个较高的 z-index 值 */
}

.bot-icon {
  cursor: pointer;
}

.chat-container {
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 600px;
  height: 550px;
  position: relative;
  background-color: #f9f9f9;
}

.chat-header {
  background-color: #f0f0f0;
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

.close-btn {
  border: none;
  background-color: transparent;
  font-size: 1.2rem;
  cursor: pointer;
  position: absolute;
  top: 10px;
  right: 10px;
}

.chat-messages {
  padding: 10px;
  max-height: 450px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  background-color: #fff; /* 将消息框内部的背景颜色设置为白色 */
}

.message {
  margin: 5px auto;
  max-width: 70%;
  display: flex; /* Add this line */
  justify-content: space-between; /* Add this line */

}

.user-message {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  text-align: right; /* 将文本内容右对齐 */

}

.bot-message {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left; /* 将文本内容左对齐 */
}

.message-info {
  font-size: 0.8rem;
  color: #999;
}

.message-text {
  background-color: #fff;
  padding: 8px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

input {
  width: calc(100% - 85px);
  padding: 10px;
  border: none;
  border-top: 1px solid #ccc;
  position: absolute;
  bottom: 0;
  left: 0;
}

.send-btn {
  border: none;
  background-color: #007bff; /* 设置按钮的背景颜色 */
  color: #fff; /* 设置按钮文字颜色 */
  padding: 10px 15px; /* 设置按钮的内边距 */
  border-radius: 5px; /* 设置按钮的圆角 */
  position: absolute;
  bottom: 0;
  right: 0;
  margin-right: 10px; /* 设置按钮与输入框的间距 */
  cursor: pointer;
}

.send-btn:hover {
  background-color: #0056b3; /* 鼠标悬停时按钮的背景颜色 */
}
</style>
