<script>
  import { onMount, tick } from 'svelte';
  
  // State
  let messages = [
    { role: 'assistant', content: 'Hello. I am Antigravity v0.3. I have now been upgraded with Vector Memory. You can say "Remember I like cats" and later ask "What do I like?"' }
  ];
  let inputMessage = '';
  let isLoading = false;
  let chatContainer;

  const API_URL = 'http://localhost:8000/api';

  async function sendMessage() {
    if (!inputMessage.trim() || isLoading) return;

    // 1. Add User Message to UI
    messages = [...messages, { role: 'user', content: inputMessage }];
    const currentInput = inputMessage;
    inputMessage = '';
    isLoading = true;
    await tick();
    scrollToBottom();

    try {
      // 2. Send to Backend
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: currentInput })
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const data = await response.json();
      
      // 3. Add Assistant Response to UI
      messages = [...messages, { role: 'assistant', content: data.content }];
    } catch (error) {
      messages = [...messages, { role: 'system', content: `Error: ${error.message}` }];
    } finally {
      isLoading = false;
      await tick();
      scrollToBottom();
    }
  }

  function scrollToBottom() {
    if (chatContainer) chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function handleKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }
</script>

<div class="chat-interface">
  <div class="messages" bind:this={chatContainer}>
    {#each messages as msg}
      <div class="message-row {msg.role}">
        <div class="avatar">{msg.role === 'assistant' ? '🤖' : msg.role === 'user' ? '👤' : '⚠️'}</div>
        <div class="bubble">
          {msg.content}
        </div>
      </div>
    {/each}
    {#if isLoading}
      <div class="message-row assistant">
        <div class="avatar">🤖</div>
        <div class="bubble typing">
          <span>.</span><span>.</span><span>.</span>
        </div>
      </div>
    {/if}
  </div>

  <div class="input-area">
    <textarea
      bind:value={inputMessage}
      on:keydown={handleKeydown}
      placeholder="Type a message to the Agent..."
      rows="1"
    ></textarea>
    <button on:click={sendMessage} disabled={isLoading || !inputMessage.trim()}>
      Send
    </button>
  </div>
</div>

<style>
  .chat-interface {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: #0f172a;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #334155;
  }

  .messages {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .message-row {
    display: flex;
    gap: 0.75rem;
    max-width: 80%;
  }

  .message-row.user {
    align-self: flex-end;
    flex-direction: row-reverse;
  }

  .avatar {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #1e293b;
    border-radius: 50%;
    font-size: 1.2rem;
    border: 1px solid #334155;
  }

  .bubble {
    padding: 0.75rem 1rem;
    border-radius: 12px;
    font-size: 0.95rem;
    line-height: 1.5;
    position: relative;
    word-wrap: break-word;
  }

  .assistant .bubble {
    background: #1e293b;
    color: #e2e8f0;
    border-top-left-radius: 2px;
  }

  .user .bubble {
    background: #2563eb;
    color: white;
    border-top-right-radius: 2px;
  }
  
  .system .bubble {
    background: #450a0a;
    color: #fca5a5;
    border: 1px solid #7f1d1d;
  }

  .input-area {
    padding: 1rem;
    background: #1e293b;
    border-top: 1px solid #334155;
    display: flex;
    gap: 0.75rem;
    align-items: flex-end;
  }

  textarea {
    flex: 1;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 0.75rem;
    color: white;
    font-family: inherit;
    resize: none;
    min-height: 44px;
    max-height: 150px;
  }

  textarea:focus {
    outline: none;
    border-color: #60a5fa;
  }

  button {
    background: #2563eb;
    color: white;
    border: none;
    padding: 0 1.5rem;
    height: 44px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
  }

  button:hover:not(:disabled) { background: #1d4ed8; }
  button:disabled { background: #334155; color: #94a3b8; cursor: not-allowed; }

  /* Typing Animation */
  .typing { display: flex; gap: 4px; padding: 1rem 1.2rem; }
  .typing span {
    width: 6px; height: 6px; background: #94a3b8; border-radius: 50%;
    animation: bounce 1.4s infinite ease-in-out both;
  }
  .typing span:nth-child(1) { animation-delay: -0.32s; }
  .typing span:nth-child(2) { animation-delay: -0.16s; }
  
  @keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
  }
</style>
