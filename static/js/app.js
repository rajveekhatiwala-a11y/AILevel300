// Enterprise RAG Document Q&A System - Frontend JavaScript

// API endpoints
const API_BASE = '';
const API_ENDPOINTS = {
    health: `${API_BASE}/api/health`,
    ingest: `${API_BASE}/api/ingest`,
    query: `${API_BASE}/api/query`,
    config: `${API_BASE}/api/config`,
    setupIndex: `${API_BASE}/api/setup-index`
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    loadConfig();
});

// Check system health
async function checkHealth() {
    try {
        const response = await fetch(API_ENDPOINTS.health);
        const data = await response.json();
        updateStatus(data.status === 'healthy', data.message);
    } catch (error) {
        updateStatus(false, 'System offline');
    }
}

// Update status indicator
function updateStatus(isHealthy, message) {
    const statusIndicator = document.getElementById('statusIndicator');
    const statusDot = statusIndicator.querySelector('.status-dot');
    const statusText = statusIndicator.querySelector('.status-text');
    
    if (isHealthy) {
        statusDot.style.background = 'var(--success-color)';
        statusText.textContent = message || 'Ready';
    } else {
        statusDot.style.background = 'var(--error-color)';
        statusText.textContent = message || 'Offline';
    }
}

// Load configuration
async function loadConfig() {
    try {
        const response = await fetch(API_ENDPOINTS.config);
        const config = await response.json();
        
        const configStatus = document.getElementById('configStatus');
        if (config.azure_configured) {
            configStatus.innerHTML = '✅ Azure Configured';
            configStatus.style.background = '#e8f5e9';
            configStatus.style.color = 'var(--success-color)';
        } else {
            configStatus.innerHTML = '⚠️ Configure Azure Settings';
            configStatus.style.background = '#fff3e0';
            configStatus.style.color = 'var(--warning-color)';
        }
    } catch (error) {
        console.error('Error loading config:', error);
    }
}

// Show configuration details
async function showConfig() {
    try {
        const response = await fetch(API_ENDPOINTS.config);
        const config = await response.json();
        
        const message = `
System Configuration:
━━━━━━━━━━━━━━━━━━━━━━━━
📁 Document Path: ${config.document_path}
📊 Chunk Size: ${config.chunk_size}
🔗 Chunk Overlap: ${config.chunk_overlap}
🎯 Top Results: ${config.top_k_results}
☁️ Azure Status: ${config.azure_configured ? '✅ Configured' : '❌ Not Configured'}
        `.trim();
        
        alert(message);
    } catch (error) {
        showError('Failed to load configuration');
    }
}

// Ingest documents
async function ingestDocuments() {
    const ingestBtn = document.getElementById('ingestBtn');
    ingestBtn.disabled = true;
    
    showLoading('Ingesting documents...');
    
    try {
        const response = await fetch(API_ENDPOINTS.ingest, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) {
            throw new Error('Ingestion failed');
        }
        
        const result = await response.json();
        hideLoading();
        
        // Show success message
        addSystemMessage('✅ ' + result.message);
        updateStatus(true, 'Documents indexed');
        
    } catch (error) {
        hideLoading();
        showError('Failed to ingest documents: ' + error.message);
    } finally {
        ingestBtn.disabled = false;
    }
}

// Submit question
async function submitQuestion() {
    const input = document.getElementById('questionInput');
    const question = input.value.trim();
    
    if (!question) {
        return;
    }
    
    // Disable input while processing
    input.disabled = true;
    document.getElementById('sendBtn').disabled = true;
    
    // Add user message
    addUserMessage(question);
    input.value = '';
    
    // Show typing indicator
    const typingId = addTypingIndicator();
    
    try {
        const response = await fetch(API_ENDPOINTS.query, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });
        
        if (!response.ok) {
            throw new Error('Query failed');
        }
        
        const result = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        // Add assistant response
        addAssistantMessage(result.answer, result.sources, result.context_chunks);
        
    } catch (error) {
        removeTypingIndicator(typingId);
        addAssistantMessage('Sorry, I encountered an error processing your question. Please try again.');
        showError(error.message);
    } finally {
        input.disabled = false;
        document.getElementById('sendBtn').disabled = false;
        input.focus();
    }
}

// Ask predefined question
function askQuestion(question) {
    document.getElementById('questionInput').value = question;
    submitQuestion();
}

// Add user message to chat
function addUserMessage(text) {
    const messagesContainer = document.getElementById('chatMessages');
    
    // Remove welcome message if present
    const welcomeMsg = messagesContainer.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message message-user';
    messageDiv.innerHTML = `
        <div class="message-bubble">
            ${escapeHtml(text)}
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Add assistant message to chat
function addAssistantMessage(text, sources = [], contextChunks = 0) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message message-assistant';
    
    let sourcesHtml = '';
    if (sources && sources.length > 0) {
        const sourceItems = sources.map(source => 
            `<li class="source-item">📄 ${escapeHtml(source)}</li>`
        ).join('');
        
        sourcesHtml = `
            <div class="message-sources">
                <h4>📚 Sources (${contextChunks} chunks):</h4>
                <ul class="source-list">${sourceItems}</ul>
            </div>
        `;
    }
    
    messageDiv.innerHTML = `
        <div class="message-bubble">
            ${formatText(text)}
            ${sourcesHtml}
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Add system message
function addSystemMessage(text) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    messageDiv.innerHTML = `
        <div class="message-bubble" style="background: #e8f5e9; color: #2e7d32; text-align: center; margin: 10px auto; max-width: 80%;">
            ${escapeHtml(text)}
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Add typing indicator
function addTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    
    const id = 'typing-' + Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.id = id;
    messageDiv.className = 'message message-assistant';
    messageDiv.innerHTML = `
        <div class="message-bubble">
            <div style="display: flex; gap: 5px; align-items: center;">
                <div class="typing-dot" style="animation: typingDot 1.4s infinite;"></div>
                <div class="typing-dot" style="animation: typingDot 1.4s infinite 0.2s;"></div>
                <div class="typing-dot" style="animation: typingDot 1.4s infinite 0.4s;"></div>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
    
    return id;
}

// Remove typing indicator
function removeTypingIndicator(id) {
    const indicator = document.getElementById(id);
    if (indicator) {
        indicator.remove();
    }
}

// Show loading modal
function showLoading(text = 'Processing...') {
    const modal = document.getElementById('loadingModal');
    const loadingText = document.getElementById('loadingText');
    loadingText.textContent = text;
    modal.classList.add('active');
}

// Hide loading modal
function hideLoading() {
    const modal = document.getElementById('loadingModal');
    modal.classList.remove('active');
}

// Show error message
function showError(message) {
    alert('❌ Error: ' + message);
}

// Handle Enter key in textarea
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        submitQuestion();
    }
}

// Scroll chat to bottom
function scrollToBottom() {
    const messagesContainer = document.getElementById('chatMessages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Format text (preserve line breaks and basic formatting)
function formatText(text) {
    return escapeHtml(text)
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/^(.+)$/, '<p>$1</p>');
}

// Add CSS for typing animation
const style = document.createElement('style');
style.textContent = `
    .typing-dot {
        width: 8px;
        height: 8px;
        background: var(--text-secondary);
        border-radius: 50%;
    }
    
    @keyframes typingDot {
        0%, 60%, 100% {
            opacity: 0.3;
            transform: translateY(0);
        }
        30% {
            opacity: 1;
            transform: translateY(-5px);
        }
    }
`;
document.head.appendChild(style);
