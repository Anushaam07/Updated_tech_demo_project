// // Application State
// const state = {
//     documents: [],
//     selectedDocument: null,
//     messages: [],
//     settings: {
//         model: 'azure-gpt4o-mini',
//         k: 4,
//         temperature: 0.7
//     }
// };

// // DOM Elements
// const elements = {
//     uploadArea: document.getElementById('uploadArea'),
//     fileInput: document.getElementById('fileInput'),
//     uploadProgress: document.getElementById('uploadProgress'),
//     progressFill: document.getElementById('progressFill'),
//     progressText: document.getElementById('progressText'),
//     documentsList: document.getElementById('documentsList'),
//     messagesContainer: document.getElementById('messagesContainer'),
//     messageInput: document.getElementById('messageInput'),
//     sendButton: document.getElementById('sendButton'),
//     clearChat: document.getElementById('clearChat'),
//     modelSelect: document.getElementById('modelSelect'),
//     kValue: document.getElementById('kValue'),
//     temperature: document.getElementById('temperature'),
//     tempValue: document.getElementById('tempValue'),
//     selectedDocInfo: document.getElementById('selectedDocInfo'),
//     selectedDocName: document.getElementById('selectedDocName'),
//     deselectDoc: document.getElementById('deselectDoc'),
//     docModal: document.getElementById('docModal'),
//     modalTitle: document.getElementById('modalTitle'),
//     modalBody: document.getElementById('modalBody'),
//     closeModal: document.getElementById('closeModal'),
//     // Advanced RAG Operations
//     ragOpsHeader: document.getElementById('ragOpsHeader'),
//     ragOpsContent: document.getElementById('ragOpsContent'),
//     embedFile: document.getElementById('embedFile'),
//     embedFileId: document.getElementById('embedFileId'),
//     embedEntityId: document.getElementById('embedEntityId'),
//     generateEmbedId: document.getElementById('generateEmbedId'),
//     directEmbedBtn: document.getElementById('directEmbedBtn'),
//     queryText: document.getElementById('queryText'),
//     queryFileId: document.getElementById('queryFileId'),
//     queryEntityId: document.getElementById('queryEntityId'),
//     queryK: document.getElementById('queryK'),
//     directQueryBtn: document.getElementById('directQueryBtn'),
//     ragResults: document.getElementById('ragResults'),
//     ragResultsContent: document.getElementById('ragResultsContent')
// };

// // Initialize App
// function init() {
//     setupEventListeners();
//     loadDocuments();
//     autoResizeTextarea();
// }

// // Event Listeners
// function setupEventListeners() {
//     // Upload
//     elements.uploadArea.addEventListener('click', () => elements.fileInput.click());
//     elements.uploadArea.addEventListener('dragover', handleDragOver);
//     elements.uploadArea.addEventListener('drop', handleDrop);
//     elements.fileInput.addEventListener('change', handleFileSelect);

//     // Chat
//     elements.sendButton.addEventListener('click', sendMessage);
//     elements.messageInput.addEventListener('keydown', handleKeyDown);
//     elements.messageInput.addEventListener('input', handleInputChange);
//     elements.clearChat.addEventListener('click', clearChat);

//     // Settings
//     elements.modelSelect.addEventListener('change', (e) => {
//         state.settings.model = e.target.value;
//     });
//     elements.kValue.addEventListener('change', (e) => {
//         state.settings.k = parseInt(e.target.value);
//     });
//     elements.temperature.addEventListener('input', (e) => {
//         state.settings.temperature = parseFloat(e.target.value);
//         elements.tempValue.textContent = e.target.value;
//     });

//     // Document selection
//     elements.deselectDoc.addEventListener('click', deselectDocument);

//     // Modal
//     elements.closeModal.addEventListener('click', closeModal);
//     elements.docModal.addEventListener('click', (e) => {
//         if (e.target === elements.docModal) closeModal();
//     });

//     // Advanced RAG Operations
//     elements.ragOpsHeader.addEventListener('click', toggleRagOpsSection);
//     elements.generateEmbedId.addEventListener('click', generateAndSetEmbedId);
//     elements.directEmbedBtn.addEventListener('click', handleDirectEmbed);
//     elements.directQueryBtn.addEventListener('click', handleDirectQuery);
// }

// // File Upload Handlers
// function handleDragOver(e) {
//     e.preventDefault();
//     e.stopPropagation();
//     elements.uploadArea.style.borderColor = 'var(--primary)';
// }

// function handleDrop(e) {
//     e.preventDefault();
//     e.stopPropagation();
//     elements.uploadArea.style.borderColor = 'var(--border)';

//     const files = e.dataTransfer.files;
//     if (files.length > 0) {
//         uploadFile(files[0]);
//     }
// }

// function handleFileSelect(e) {
//     const files = e.target.files;
//     if (files.length > 0) {
//         uploadFile(files[0]);
//     }
// }

// async function uploadFile(file) {
//     const fileId = generateFileId();
//     const formData = new FormData();
//     formData.append('file', file);
//     formData.append('file_id', fileId);
//     formData.append('entity_id', 'default_user');

//     showUploadProgress();

//     try {
//         const response = await fetch('/embed', {
//             method: 'POST',
//             body: formData
//         });

//         if (!response.ok) {
//             throw new Error(`Upload failed: ${response.statusText}`);
//         }

//         const result = await response.json();

//         addDocument({
//             id: fileId,
//             name: file.name,
//             size: formatFileSize(file.size),
//             uploadedAt: new Date().toISOString(),
//             type: result.known_type || 'unknown'
//         });

//         hideUploadProgress();
//         showSystemMessage(`Successfully uploaded: ${file.name}`);

//         // Auto-select the uploaded document
//         selectDocument(fileId);

//     } catch (error) {
//         console.error('Upload error:', error);
//         hideUploadProgress();
//         showErrorMessage(`Failed to upload file: ${error.message}`);
//     }

//     elements.fileInput.value = '';
// }

// function showUploadProgress() {
//     elements.uploadProgress.classList.remove('hidden');
//     elements.progressFill.style.width = '0%';

//     let progress = 0;
//     const interval = setInterval(() => {
//         progress += 10;
//         elements.progressFill.style.width = `${Math.min(progress, 90)}%`;
//         elements.progressText.textContent = `Uploading... ${Math.min(progress, 90)}%`;

//         if (progress >= 90) {
//             clearInterval(interval);
//         }
//     }, 200);
// }

// function hideUploadProgress() {
//     elements.progressFill.style.width = '100%';
//     elements.progressText.textContent = 'Upload complete!';

//     setTimeout(() => {
//         elements.uploadProgress.classList.add('hidden');
//     }, 1000);
// }

// // Document Management
// async function loadDocuments() {
//     try {
//         const response = await fetch('/ids');
//         const ids = await response.json();

//         // For now, we'll just store the IDs
//         // In a real app, you'd fetch metadata for each document
//         ids.forEach(id => {
//             if (!state.documents.find(doc => doc.id === id)) {
//                 addDocument({
//                     id: id,
//                     name: `Document ${id.substring(0, 8)}`,
//                     size: 'N/A',
//                     uploadedAt: new Date().toISOString(),
//                     type: 'unknown'
//                 }, false);
//             }
//         });

//         renderDocuments();
//     } catch (error) {
//         console.error('Error loading documents:', error);
//     }
// }

// function addDocument(doc, render = true) {
//     state.documents.push(doc);
//     if (render) {
//         renderDocuments();
//     }
// }

// function renderDocuments() {
//     if (state.documents.length === 0) {
//         elements.documentsList.innerHTML = '<p class="empty-state">No documents uploaded yet</p>';
//         return;
//     }

//     elements.documentsList.innerHTML = state.documents.map(doc => `
//         <div class="document-item ${state.selectedDocument?.id === doc.id ? 'selected' : ''}"
//              data-doc-id="${doc.id}">
//             <div class="doc-info">
//                 <div class="doc-name" title="${doc.name}">
//                     <i class="fas fa-file-alt"></i> ${doc.name}
//                 </div>
//                 <div class="doc-meta">${doc.size} • ${formatDate(doc.uploadedAt)}</div>
//             </div>
//             <div class="doc-actions">
//                 <button class="btn-icon-small select-doc" title="Select for chat">
//                     <i class="fas fa-check-circle"></i>
//                 </button>
//                 <button class="btn-icon-small delete-doc" title="Delete">
//                     <i class="fas fa-trash"></i>
//                 </button>
//             </div>
//         </div>
//     `).join('');

//     // Attach event listeners
//     document.querySelectorAll('.select-doc').forEach(btn => {
//         btn.addEventListener('click', (e) => {
//             e.stopPropagation();
//             const docId = e.target.closest('.document-item').dataset.docId;
//             selectDocument(docId);
//         });
//     });

//     document.querySelectorAll('.delete-doc').forEach(btn => {
//         btn.addEventListener('click', (e) => {
//             e.stopPropagation();
//             const docId = e.target.closest('.document-item').dataset.docId;
//             deleteDocument(docId);
//         });
//     });
// }

// function selectDocument(docId) {
//     const doc = state.documents.find(d => d.id === docId);
//     if (doc) {
//         state.selectedDocument = doc;
//         elements.selectedDocInfo.style.display = 'flex';
//         elements.selectedDocName.textContent = doc.name;
//         renderDocuments();
//         enableSendButton();
//         showSystemMessage(`Selected document: ${doc.name}. You can now ask questions about it.`);
//     }
// }

// function deselectDocument() {
//     state.selectedDocument = null;
//     elements.selectedDocInfo.style.display = 'none';
//     renderDocuments();
//     checkSendButtonState();
// }

// async function deleteDocument(docId) {
//     if (!confirm('Are you sure you want to delete this document?')) {
//         return;
//     }

//     try {
//         const response = await fetch('/documents', {
//             method: 'DELETE',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify([docId])
//         });

//         if (!response.ok) {
//             throw new Error('Failed to delete document');
//         }

//         state.documents = state.documents.filter(doc => doc.id !== docId);
//         if (state.selectedDocument?.id === docId) {
//             deselectDocument();
//         }
//         renderDocuments();
//         showSystemMessage('Document deleted successfully');

//     } catch (error) {
//         console.error('Delete error:', error);
//         showErrorMessage('Failed to delete document');
//     }
// }

// // Chat Functionality
// function handleKeyDown(e) {
//     if (e.key === 'Enter' && !e.shiftKey) {
//         e.preventDefault();
//         sendMessage();
//     }
// }

// function handleInputChange() {
//     autoResizeTextarea();
//     checkSendButtonState();
// }

// function autoResizeTextarea() {
//     elements.messageInput.style.height = 'auto';
//     elements.messageInput.style.height = elements.messageInput.scrollHeight + 'px';
// }

// function checkSendButtonState() {
//     const hasText = elements.messageInput.value.trim().length > 0;
//     const hasDoc = state.selectedDocument !== null;
//     elements.sendButton.disabled = !(hasText && hasDoc);
// }

// function enableSendButton() {
//     checkSendButtonState();
// }

// async function sendMessage() {
//     const message = elements.messageInput.value.trim();
//     if (!message || !state.selectedDocument) return;

//     // Add user message
//     addMessage({
//         role: 'user',
//         content: message,
//         timestamp: new Date().toISOString()
//     });

//     elements.messageInput.value = '';
//     autoResizeTextarea();
//     checkSendButtonState();

//     // Show typing indicator
//     const typingId = addTypingIndicator();

//     try {
//         const response = await fetch('/chat', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({
//                 query: message,
//                 file_id: state.selectedDocument.id,
//                 model: state.settings.model,
//                 k: state.settings.k,
//                 temperature: state.settings.temperature
//             })
//         });

//         removeMessage(typingId);

//         if (!response.ok) {
//              // Extract the detailed error message from the response

//             const errorData = await response.json().catch(() => ({}));
//             const errorMessage = errorData.detail || response.statusText;
//             throw new Error(errorMessage);
//         }

//         const result = await response.json();

//         // Add assistant message
//         addMessage({
//             role: 'assistant',
//             content: result.answer,
//             sources: result.sources,
//             timestamp: new Date().toISOString()
//         });

//     } catch (error) {
//         console.error('Chat error:', error);
//         removeMessage(typingId);
//         showErrorMessage(`Failed to get response: ${error.message}`);
//     }
// }

// function addMessage(message) {
//     // Remove welcome message if it exists
//     const welcomeMsg = elements.messagesContainer.querySelector('.welcome-message');
//     if (welcomeMsg) {
//         welcomeMsg.remove();
//     }

//     state.messages.push(message);
//     renderMessage(message);
//     scrollToBottom();
// }

// function renderMessage(message) {
//     const messageEl = document.createElement('div');
//     messageEl.className = `message ${message.role}`;
//     messageEl.dataset.messageId = message.timestamp;

//     const avatarIcon = {
//         user: 'fa-user',
//         assistant: 'fa-robot',
//         system: 'fa-info-circle',
//         error: 'fa-exclamation-triangle',
//         typing: 'fa-robot'
//     }[message.role] || 'fa-circle';

//     let sourcesHtml = '';
//     if (message.sources && message.sources.length > 0) {
//         sourcesHtml = `
//             <div class="message-sources">
//                 <h4><i class="fas fa-book"></i> Sources:</h4>
//                 ${message.sources.map((source, idx) => `
//                     <div class="source-item">
//                         <strong>Source ${idx + 1}</strong>
//                         <span class="source-score">(Score: ${source.score.toFixed(3)})</span>
//                         <p>${truncateText(source.content, 150)}</p>
//                     </div>
//                 `).join('')}
//             </div>
//         `;
//     }

//     messageEl.innerHTML = `
//         <div class="message-avatar">
//             <i class="fas ${avatarIcon}"></i>
//         </div>
//         <div class="message-content">
//             <div class="message-header">
//                 <span class="message-role">${capitalizeFirst(message.role)}</span>
//                 <span class="message-time">${formatTime(message.timestamp)}</span>
//             </div>
//             <div class="message-text">
//                 ${message.content || '<div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>'}
//             </div>
//             ${sourcesHtml}
//         </div>
//     `;

//     elements.messagesContainer.appendChild(messageEl);
// }

// function addTypingIndicator() {
//     const typingMessage = {
//         role: 'typing',
//         content: null,
//         timestamp: Date.now().toString()
//     };
//     addMessage(typingMessage);
//     return typingMessage.timestamp;
// }

// function removeMessage(messageId) {
//     const messageEl = elements.messagesContainer.querySelector(`[data-message-id="${messageId}"]`);
//     if (messageEl) {
//         messageEl.remove();
//     }
//     state.messages = state.messages.filter(m => m.timestamp !== messageId);
// }

// function showSystemMessage(text) {
//     addMessage({
//         role: 'system',
//         content: text,
//         timestamp: new Date().toISOString()
//     });
// }

// function showErrorMessage(text) {
//     addMessage({
//         role: 'error',
//         content: text,
//         timestamp: new Date().toISOString()
//     });
// }

// function clearChat() {
//     if (state.messages.length === 0) return;

//     if (confirm('Are you sure you want to clear the chat history?')) {
//         state.messages = [];
//         elements.messagesContainer.innerHTML = `
//             <div class="welcome-message">
//                 <i class="fas fa-info-circle"></i>
//                 <h2>Chat Cleared</h2>
//                 <p>Select a document and start asking questions!</p>
//             </div>
//         `;
//     }
// }

// function scrollToBottom() {
//     setTimeout(() => {
//         elements.messagesContainer.scrollTop = elements.messagesContainer.scrollHeight;
//     }, 100);
// }

// // Modal Functions
// function closeModal() {
//     elements.docModal.classList.add('hidden');
// }

// // Advanced RAG Operations Functions
// function toggleRagOpsSection() {
//     const content = elements.ragOpsContent;
//     const icon = elements.ragOpsHeader.querySelector('.toggle-icon');

//     if (content.classList.contains('expanded')) {
//         content.classList.remove('expanded');
//         icon.classList.remove('rotated');
//     } else {
//         content.classList.add('expanded');
//         icon.classList.add('rotated');
//     }
// }

// function generateAndSetEmbedId() {
//     const fileId = generateFileId();
//     elements.embedFileId.value = fileId;
// }

// async function handleDirectEmbed() {
//     const file = elements.embedFile.files[0];
//     const fileId = elements.embedFileId.value.trim();
//     const entityId = elements.embedEntityId.value.trim();

//     if (!file) {
//         showRagError('Please select a file to embed');
//         return;
//     }

//     if (!fileId) {
//         showRagError('Please provide a File ID (or click Generate)');
//         return;
//     }

//     const formData = new FormData();
//     formData.append('file', file);
//     formData.append('file_id', fileId);
//     if (entityId) {
//         formData.append('entity_id', entityId);
//     }

//     elements.directEmbedBtn.disabled = true;
//     elements.directEmbedBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Embedding...';

//     try {
//         const response = await fetch('/embed', {
//             method: 'POST',
//             body: formData
//         });

//         if (!response.ok) {
//             const error = await response.json();
//             throw new Error(error.detail || 'Failed to embed document');
//         }

//         const result = await response.json();

//         showRagSuccess(`Document embedded successfully!<br>
//             <strong>File ID:</strong> ${fileId}<br>
//             <strong>Filename:</strong> ${result.filename}<br>
//             <strong>Type:</strong> ${result.known_type || 'unknown'}`);

//         // Clear form
//         elements.embedFile.value = '';
//         elements.embedFileId.value = '';

//         // Reload documents list
//         await loadDocuments();

//     } catch (error) {
//         console.error('Embed error:', error);
//         showRagError(`Failed to embed: ${error.message}`);
//     } finally {
//         elements.directEmbedBtn.disabled = false;
//         elements.directEmbedBtn.innerHTML = '<i class="fas fa-cloud-upload-alt"></i> Embed Document';
//     }
// }

// async function handleDirectQuery() {
//     const query = elements.queryText.value.trim();
//     const fileId = elements.queryFileId.value.trim();
//     const entityId = elements.queryEntityId.value.trim();
//     const k = parseInt(elements.queryK.value);

//     if (!query) {
//         showRagError('Please enter a query');
//         return;
//     }

//     if (!fileId) {
//         showRagError('Please provide a File ID');
//         return;
//     }

//     elements.directQueryBtn.disabled = true;
//     elements.directQueryBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Querying...';

//     try {
//         const requestBody = {
//             query: query,
//             file_id: fileId,
//             k: k
//         };

//         if (entityId) {
//             requestBody.entity_id = entityId;
//         }

//         const response = await fetch('/query', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify(requestBody)
//         });

//         if (!response.ok) {
//             const error = await response.json();
//             throw new Error(error.detail || 'Query failed');
//         }

//         const results = await response.json();
//         displayQueryResults(results, query, fileId);

//     } catch (error) {
//         console.error('Query error:', error);
//         showRagError(`Query failed: ${error.message}`);
//     } finally {
//         elements.directQueryBtn.disabled = false;
//         elements.directQueryBtn.innerHTML = '<i class="fas fa-search"></i> Query Documents';
//     }
// }

// function displayQueryResults(results, query, fileId) {
//     elements.ragResults.classList.remove('hidden');

//     if (!results || results.length === 0) {
//         elements.ragResultsContent.innerHTML = `
//             <div class="error-message">
//                 No results found for query "${query}" in file "${fileId}"
//             </div>
//         `;
//         return;
//     }

//     let html = `
//         <div class="success-message" style="margin-bottom: 1rem;">
//             Found ${results.length} result(s) for query: <strong>"${query}"</strong>
//         </div>
//     `;

//     results.forEach((item, idx) => {
//         const [document, score] = item;
//         const content = document.page_content || document.content || 'No content';
//         const metadata = document.metadata || {};

//         html += `
//             <div class="result-item">
//                 <div class="result-meta">
//                     <strong>Result ${idx + 1}</strong> |
//                     Score: <span class="result-score">${score.toFixed(4)}</span>
//                     ${metadata.page ? ` | Page: ${metadata.page}` : ''}
//                 </div>
//                 <div class="result-content">${truncateText(content, 200)}</div>
//             </div>
//         `;
//     });

//     elements.ragResultsContent.innerHTML = html;

//     // Scroll to results
//     elements.ragResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
// }

// function showRagSuccess(message) {
//     elements.ragResults.classList.remove('hidden');
//     elements.ragResultsContent.innerHTML = `
//         <div class="success-message">${message}</div>
//     `;
//     setTimeout(() => {
//         elements.ragResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
//     }, 100);
// }

// function showRagError(message) {
//     elements.ragResults.classList.remove('hidden');
//     elements.ragResultsContent.innerHTML = `
//         <div class="error-message">${message}</div>
//     `;
//     setTimeout(() => {
//         elements.ragResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
//     }, 100);
// }

// // Utility Functions
// function generateFileId() {
//     return 'file_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
// }

// function formatFileSize(bytes) {
//     if (bytes === 0) return '0 B';
//     const k = 1024;
//     const sizes = ['B', 'KB', 'MB', 'GB'];
//     const i = Math.floor(Math.log(bytes) / Math.log(k));
//     return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
// }

// function formatDate(isoString) {
//     const date = new Date(isoString);
//     const now = new Date();
//     const diffMs = now - date;
//     const diffMins = Math.floor(diffMs / 60000);

//     if (diffMins < 1) return 'Just now';
//     if (diffMins < 60) return `${diffMins} min ago`;
//     if (diffMins < 1440) return `${Math.floor(diffMins / 60)} hours ago`;

//     return date.toLocaleDateString();
// }

// function formatTime(isoString) {
//     const date = new Date(isoString);
//     return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
// }

// function capitalizeFirst(str) {
//     return str.charAt(0).toUpperCase() + str.slice(1);
// }

// function truncateText(text, maxLength) {
//     if (text.length <= maxLength) return text;
//     return text.substring(0, maxLength) + '...';
// }

// // Initialize app when DOM is ready
// if (document.readyState === 'loading') {
//     document.addEventListener('DOMContentLoaded', init);
// } else {
//     init();
// }





// Application State
const state = {
    documents: [],
    selectedDocument: null,
    messages: [],
    settings: {
        model: 'azure-gpt4o-mini',
        k: 4,
        temperature: 0.7,
        guardrailsEnabled: true  // Toggle for demo purposes
    }
};

// DOM Elements
const elements = {
    uploadArea: document.getElementById('uploadArea'),
    fileInput: document.getElementById('fileInput'),
    uploadProgress: document.getElementById('uploadProgress'),
    progressFill: document.getElementById('progressFill'),
    progressText: document.getElementById('progressText'),
    documentsList: document.getElementById('documentsList'),
    messagesContainer: document.getElementById('messagesContainer'),
    messageInput: document.getElementById('messageInput'),
    sendButton: document.getElementById('sendButton'),
    clearChat: document.getElementById('clearChat'),
    modelSelect: document.getElementById('modelSelect'),
    kValue: document.getElementById('kValue'),
    temperature: document.getElementById('temperature'),
    tempValue: document.getElementById('tempValue'),
    selectedDocInfo: document.getElementById('selectedDocInfo'),
    selectedDocName: document.getElementById('selectedDocName'),
    deselectDoc: document.getElementById('deselectDoc'),
    docModal: document.getElementById('docModal'),
    modalTitle: document.getElementById('modalTitle'),
    modalBody: document.getElementById('modalBody'),
    closeModal: document.getElementById('closeModal'),
    // Advanced RAG Operations
    ragOpsHeader: document.getElementById('ragOpsHeader'),
    ragOpsContent: document.getElementById('ragOpsContent'),
    embedFile: document.getElementById('embedFile'),
    embedFileId: document.getElementById('embedFileId'),
    embedEntityId: document.getElementById('embedEntityId'),
    generateEmbedId: document.getElementById('generateEmbedId'),
    directEmbedBtn: document.getElementById('directEmbedBtn'),
    queryText: document.getElementById('queryText'),
    queryFileId: document.getElementById('queryFileId'),
    queryEntityId: document.getElementById('queryEntityId'),
    queryK: document.getElementById('queryK'),
    directQueryBtn: document.getElementById('directQueryBtn'),
    ragResults: document.getElementById('ragResults'),
    ragResultsContent: document.getElementById('ragResultsContent'),
    // Demo toggle
    demoModeToggle: document.getElementById('demoModeToggle'),
    demoModeStatus: document.getElementById('demoModeStatus')
};

// Initialize App
function init() {
    setupEventListeners();
    loadDocuments();
    autoResizeTextarea();
}

// Event Listeners
function setupEventListeners() {
    // Upload
    elements.uploadArea.addEventListener('click', () => elements.fileInput.click());
    elements.uploadArea.addEventListener('dragover', handleDragOver);
    elements.uploadArea.addEventListener('drop', handleDrop);
    elements.fileInput.addEventListener('change', handleFileSelect);

    // Chat
    elements.sendButton.addEventListener('click', sendMessage);
    elements.messageInput.addEventListener('keydown', handleKeyDown);
    elements.messageInput.addEventListener('input', handleInputChange);
    elements.clearChat.addEventListener('click', clearChat);

    // Settings
    elements.modelSelect.addEventListener('change', (e) => {
        state.settings.model = e.target.value;
    });
    elements.kValue.addEventListener('change', (e) => {
        state.settings.k = parseInt(e.target.value);
    });
    elements.temperature.addEventListener('input', (e) => {
        state.settings.temperature = parseFloat(e.target.value);
        elements.tempValue.textContent = e.target.value;
    });

    // Document selection
    elements.deselectDoc.addEventListener('click', deselectDocument);

    // Modal
    elements.closeModal.addEventListener('click', closeModal);
    elements.docModal.addEventListener('click', (e) => {
        if (e.target === elements.docModal) closeModal();
    });

    // Advanced RAG Operations
    elements.ragOpsHeader.addEventListener('click', toggleRagOpsSection);
    elements.generateEmbedId.addEventListener('click', generateAndSetEmbedId);
    elements.directEmbedBtn.addEventListener('click', handleDirectEmbed);
    elements.directQueryBtn.addEventListener('click', handleDirectQuery);

    // Demo mode toggle
    elements.demoModeToggle.addEventListener('change', handleDemoModeToggle);
}

function handleDemoModeToggle(e) {
    state.settings.guardrailsEnabled = e.target.checked;

    if (state.settings.guardrailsEnabled) {
        elements.demoModeStatus.textContent = 'Protected ';
        elements.demoModeStatus.className = 'demo-status protected';
        showSystemMessage(' Guardrails ENABLED');
    } else {
        elements.demoModeStatus.textContent = 'UNSAFE ';
        elements.demoModeStatus.className = 'demo-status unsafe';
        showSystemMessage('Guardrails DISABLED');
    }
}

// File Upload Handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    elements.uploadArea.style.borderColor = 'var(--primary)';
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    elements.uploadArea.style.borderColor = 'var(--border)';

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        uploadFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        uploadFile(files[0]);
    }
}

async function uploadFile(file) {
    const fileId = generateFileId();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('file_id', fileId);
    formData.append('entity_id', 'default_user');

    showUploadProgress();

    try {
        const response = await fetch('/embed', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }

        const result = await response.json();

        addDocument({
            id: fileId,
            name: file.name,
            size: formatFileSize(file.size),
            uploadedAt: new Date().toISOString(),
            type: result.known_type || 'unknown'
        });

        hideUploadProgress();
        showSystemMessage(`Successfully uploaded: ${file.name}`);

        // Auto-select the uploaded document
        selectDocument(fileId);

    } catch (error) {
        console.error('Upload error:', error);
        hideUploadProgress();
        showErrorMessage(`Failed to upload file: ${error.message}`);
    }

    elements.fileInput.value = '';
}

function showUploadProgress() {
    elements.uploadProgress.classList.remove('hidden');
    elements.progressFill.style.width = '0%';

    let progress = 0;
    const interval = setInterval(() => {
        progress += 10;
        elements.progressFill.style.width = `${Math.min(progress, 90)}%`;
        elements.progressText.textContent = `Uploading... ${Math.min(progress, 90)}%`;

        if (progress >= 90) {
            clearInterval(interval);
        }
    }, 200);
}

function hideUploadProgress() {
    elements.progressFill.style.width = '100%';
    elements.progressText.textContent = 'Upload complete!';

    setTimeout(() => {
        elements.uploadProgress.classList.add('hidden');
    }, 1000);
}

// Document Management
async function loadDocuments() {
    try {
        const response = await fetch('/ids');
        const ids = await response.json();

        // For now, we'll just store the IDs
        // In a real app, you'd fetch metadata for each document
        ids.forEach(id => {
            if (!state.documents.find(doc => doc.id === id)) {
                addDocument({
                    id: id,
                    name: `Document ${id.substring(0, 8)}`,
                    size: 'N/A',
                    uploadedAt: new Date().toISOString(),
                    type: 'unknown'
                }, false);
            }
        });

        renderDocuments();
    } catch (error) {
        console.error('Error loading documents:', error);
    }
}

function addDocument(doc, render = true) {
    state.documents.push(doc);
    if (render) {
        renderDocuments();
    }
}

function renderDocuments() {
    if (state.documents.length === 0) {
        elements.documentsList.innerHTML = '<p class="empty-state">No documents uploaded yet</p>';
        return;
    }

    elements.documentsList.innerHTML = state.documents.map(doc => `
        <div class="document-item ${state.selectedDocument?.id === doc.id ? 'selected' : ''}"
             data-doc-id="${doc.id}">
            <div class="doc-info">
                <div class="doc-name" title="${doc.name}">
                    <i class="fas fa-file-alt"></i> ${doc.name}
                </div>
                <div class="doc-meta">${doc.size} • ${formatDate(doc.uploadedAt)}</div>
            </div>
            <div class="doc-actions">
                <button class="btn-icon-small select-doc" title="Select for chat">
                    <i class="fas fa-check-circle"></i>
                </button>
                <button class="btn-icon-small delete-doc" title="Delete">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');

    // Attach event listeners
    document.querySelectorAll('.select-doc').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const docId = e.target.closest('.document-item').dataset.docId;
            selectDocument(docId);
        });
    });

    document.querySelectorAll('.delete-doc').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const docId = e.target.closest('.document-item').dataset.docId;
            deleteDocument(docId);
        });
    });
}

function selectDocument(docId) {
    const doc = state.documents.find(d => d.id === docId);
    if (doc) {
        state.selectedDocument = doc;
        elements.selectedDocInfo.style.display = 'flex';
        elements.selectedDocName.textContent = doc.name;
        renderDocuments();
        enableSendButton();
        showSystemMessage(`Selected document: ${doc.name}. You can now ask questions about it.`);
    }
}

function deselectDocument() {
    state.selectedDocument = null;
    elements.selectedDocInfo.style.display = 'none';
    renderDocuments();
    checkSendButtonState();
}

async function deleteDocument(docId) {
    if (!confirm('Are you sure you want to delete this document?')) {
        return;
    }

    try {
        const response = await fetch('/documents', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify([docId])
        });

        if (!response.ok) {
            throw new Error('Failed to delete document');
        }

        state.documents = state.documents.filter(doc => doc.id !== docId);
        if (state.selectedDocument?.id === docId) {
            deselectDocument();
        }
        renderDocuments();
        showSystemMessage('Document deleted successfully');

    } catch (error) {
        console.error('Delete error:', error);
        showErrorMessage('Failed to delete document');
    }
}

// Chat Functionality
function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

function handleInputChange() {
    autoResizeTextarea();
    checkSendButtonState();
}

function autoResizeTextarea() {
    elements.messageInput.style.height = 'auto';
    elements.messageInput.style.height = elements.messageInput.scrollHeight + 'px';
}

function checkSendButtonState() {
    const hasText = elements.messageInput.value.trim().length > 0;
    const hasDoc = state.selectedDocument !== null;
    elements.sendButton.disabled = !(hasText && hasDoc);
}

function enableSendButton() {
    checkSendButtonState();
}

async function sendMessage() {
    const message = elements.messageInput.value.trim();
    if (!message || !state.selectedDocument) return;

    // Add user message
    addMessage({
        role: 'user',
        content: message,
        timestamp: new Date().toISOString()
    });

    elements.messageInput.value = '';
    autoResizeTextarea();
    checkSendButtonState();

    // Show typing indicator
    const typingId = addTypingIndicator();

    try {
        // Use different endpoint based on guardrails toggle
        const endpoint = state.settings.guardrailsEnabled ? '/chat' : '/chat-unsafe';

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: message,
                file_id: state.selectedDocument.id,
                model: state.settings.model,
                k: state.settings.k,
                temperature: state.settings.temperature
            })
        });

        removeMessage(typingId);

        if (!response.ok) {
            // Extract the detailed error message from the response
            const errorData = await response.json().catch(() => ({}));
            const errorMessage = errorData.detail || response.statusText;
            throw new Error(errorMessage);
        }

        const result = await response.json();

        // Add assistant message
        addMessage({
            role: 'assistant',
            content: result.answer,
            sources: result.sources,
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        console.error('Chat error:', error);
        removeMessage(typingId);
        showErrorMessage(`Failed to get response: ${error.message}`);
    }
}

function addMessage(message) {
    // Remove welcome message if it exists
    const welcomeMsg = elements.messagesContainer.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    state.messages.push(message);
    renderMessage(message);
    scrollToBottom();
}

function renderMessage(message) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${message.role}`;
    messageEl.dataset.messageId = message.timestamp;

    const avatarIcon = {
        user: 'fa-user',
        assistant: 'fa-robot',
        system: 'fa-info-circle',
        error: 'fa-exclamation-triangle',
        typing: 'fa-robot'
    }[message.role] || 'fa-circle';

    let sourcesHtml = '';
    if (message.sources && message.sources.length > 0) {
        sourcesHtml = `
            <div class="message-sources">
                <h4><i class="fas fa-book"></i> Sources:</h4>
                ${message.sources.map((source, idx) => `
                    <div class="source-item">
                        <strong>Source ${idx + 1}</strong>
                        <span class="source-score">(Score: ${source.score.toFixed(3)})</span>
                        <p>${truncateText(source.content, 150)}</p>
                    </div>
                `).join('')}
            </div>
        `;
    }

    messageEl.innerHTML = `
        <div class="message-avatar">
            <i class="fas ${avatarIcon}"></i>
        </div>
        <div class="message-content">
            <div class="message-header">
                <span class="message-role">${capitalizeFirst(message.role)}</span>
                <span class="message-time">${formatTime(message.timestamp)}</span>
            </div>
            <div class="message-text">
                ${message.content || '<div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>'}
            </div>
            ${sourcesHtml}
        </div>
    `;

    elements.messagesContainer.appendChild(messageEl);
}

function addTypingIndicator() {
    const typingMessage = {
        role: 'typing',
        content: null,
        timestamp: Date.now().toString()
    };
    addMessage(typingMessage);
    return typingMessage.timestamp;
}

function removeMessage(messageId) {
    const messageEl = elements.messagesContainer.querySelector(`[data-message-id="${messageId}"]`);
    if (messageEl) {
        messageEl.remove();
    }
    state.messages = state.messages.filter(m => m.timestamp !== messageId);
}

function showSystemMessage(text) {
    addMessage({
        role: 'system',
        content: text,
        timestamp: new Date().toISOString()
    });
}

function showErrorMessage(text) {
    addMessage({
        role: 'error',
        content: text,
        timestamp: new Date().toISOString()
    });
}

function clearChat() {
    if (state.messages.length === 0) return;

    if (confirm('Are you sure you want to clear the chat history?')) {
        state.messages = [];
        elements.messagesContainer.innerHTML = `
            <div class="welcome-message">
                <i class="fas fa-info-circle"></i>
                <h2>Chat Cleared</h2>
                <p>Select a document and start asking questions!</p>
            </div>
        `;
    }
}

function scrollToBottom() {
    setTimeout(() => {
        elements.messagesContainer.scrollTop = elements.messagesContainer.scrollHeight;
    }, 100);
}

// Modal Functions
function closeModal() {
    elements.docModal.classList.add('hidden');
}

// Advanced RAG Operations Functions
function toggleRagOpsSection() {
    const content = elements.ragOpsContent;
    const icon = elements.ragOpsHeader.querySelector('.toggle-icon');

    if (content.classList.contains('expanded')) {
        content.classList.remove('expanded');
        icon.classList.remove('rotated');
    } else {
        content.classList.add('expanded');
        icon.classList.add('rotated');
    }
}

function generateAndSetEmbedId() {
    const fileId = generateFileId();
    elements.embedFileId.value = fileId;
}

async function handleDirectEmbed() {
    const file = elements.embedFile.files[0];
    const fileId = elements.embedFileId.value.trim();
    const entityId = elements.embedEntityId.value.trim();

    if (!file) {
        showRagError('Please select a file to embed');
        return;
    }

    if (!fileId) {
        showRagError('Please provide a File ID (or click Generate)');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('file_id', fileId);
    if (entityId) {
        formData.append('entity_id', entityId);
    }

    elements.directEmbedBtn.disabled = true;
    elements.directEmbedBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Embedding...';

    try {
        const response = await fetch('/embed', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to embed document');
        }

        const result = await response.json();

        showRagSuccess(`Document embedded successfully!<br>
            <strong>File ID:</strong> ${fileId}<br>
            <strong>Filename:</strong> ${result.filename}<br>
            <strong>Type:</strong> ${result.known_type || 'unknown'}`);

        // Clear form
        elements.embedFile.value = '';
        elements.embedFileId.value = '';

        // Reload documents list
        await loadDocuments();

    } catch (error) {
        console.error('Embed error:', error);
        showRagError(`Failed to embed: ${error.message}`);
    } finally {
        elements.directEmbedBtn.disabled = false;
        elements.directEmbedBtn.innerHTML = '<i class="fas fa-cloud-upload-alt"></i> Embed Document';
    }
}

async function handleDirectQuery() {
    const query = elements.queryText.value.trim();
    const fileId = elements.queryFileId.value.trim();
    const entityId = elements.queryEntityId.value.trim();
    const k = parseInt(elements.queryK.value);

    if (!query) {
        showRagError('Please enter a query');
        return;
    }

    if (!fileId) {
        showRagError('Please provide a File ID');
        return;
    }

    elements.directQueryBtn.disabled = true;
    elements.directQueryBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Querying...';

    try {
        const requestBody = {
            query: query,
            file_id: fileId,
            k: k
        };

        if (entityId) {
            requestBody.entity_id = entityId;
        }

        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Query failed');
        }

        const results = await response.json();
        displayQueryResults(results, query, fileId);

    } catch (error) {
        console.error('Query error:', error);
        showRagError(`Query failed: ${error.message}`);
    } finally {
        elements.directQueryBtn.disabled = false;
        elements.directQueryBtn.innerHTML = '<i class="fas fa-search"></i> Query Documents';
    }
}

function displayQueryResults(results, query, fileId) {
    elements.ragResults.classList.remove('hidden');

    if (!results || results.length === 0) {
        elements.ragResultsContent.innerHTML = `
            <div class="error-message">
                No results found for query "${query}" in file "${fileId}"
            </div>
        `;
        return;
    }

    let html = `
        <div class="success-message" style="margin-bottom: 1rem;">
            Found ${results.length} result(s) for query: <strong>"${query}"</strong>
        </div>
    `;

    results.forEach((item, idx) => {
        const [document, score] = item;
        const content = document.page_content || document.content || 'No content';
        const metadata = document.metadata || {};

        html += `
            <div class="result-item">
                <div class="result-meta">
                    <strong>Result ${idx + 1}</strong> |
                    Score: <span class="result-score">${score.toFixed(4)}</span>
                    ${metadata.page ? ` | Page: ${metadata.page}` : ''}
                </div>
                <div class="result-content">${truncateText(content, 200)}</div>
            </div>
        `;
    });

    elements.ragResultsContent.innerHTML = html;

    // Scroll to results
    elements.ragResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showRagSuccess(message) {
    elements.ragResults.classList.remove('hidden');
    elements.ragResultsContent.innerHTML = `
        <div class="success-message">${message}</div>
    `;
    setTimeout(() => {
        elements.ragResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

function showRagError(message) {
    elements.ragResults.classList.remove('hidden');
    elements.ragResultsContent.innerHTML = `
        <div class="error-message">${message}</div>
    `;
    setTimeout(() => {
        elements.ragResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

// Utility Functions
function generateFileId() {
    return 'file_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDate(isoString) {
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} min ago`;
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)} hours ago`;

    return date.toLocaleDateString();
}

function formatTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}