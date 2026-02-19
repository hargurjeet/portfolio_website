async function sendQuestion() {
    const question = document.getElementById('question').value;
    const chatBox = document.getElementById('chat-box');
    
    chatBox.innerHTML += `<p><strong>You:</strong> ${question}</p>`;
    
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question})
    });
    
    const data = await response.json();
    chatBox.innerHTML += `<p><strong>Bot:</strong> ${data.answer}</p>`;
    
    document.getElementById('question').value = '';
}
