function sendQuery() {
  const msg = document.getElementById('query').value;
  fetch('/chatbot_query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: msg })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById('response').innerText = data.reply;
  });
}
