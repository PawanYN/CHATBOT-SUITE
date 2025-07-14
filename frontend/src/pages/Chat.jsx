// React and required hooks
import { useState, useRef, useEffect } from 'react';
// Bootstrap components for layout and styling
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';

function Chat() {
  // State to store messages between user and bot
  const [messages, setMessages] = useState([]);
  // State for the input text box
  const [input, setInput] = useState('');
  // Ref to automatically scroll to the latest message
  const messagesEndRef = useRef(null);

  // Auto-scrolls to the bottom when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Called when user submits a message
  const handleSend = async (e) => {
    e.preventDefault(); // Prevents page reload
    if (!input.trim()) return; // Do nothing for empty input

    // Add user's message to the message list immediately
    const userMessage = { from: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      // Send the message to your FastAPI backend
      const res = await fetch('http://localhost:7000/api/chatbot/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include', // Important to maintain session using cookies
        body: JSON.stringify({ query: input }) // Send the user input as `query`
      });
 
      // Parse JSON response from backend
      const data = await res.json();
    
        
      // Add bot's response to messages
      const botMessage = {
        from: 'bot',
        text: data.reply || 'No reply' // fallback if response is empty
      };

      setMessages((prev) => [...prev, botMessage]);

    } catch (err) {
      console.error('Chat error:', err);
      // Show error message in chat box if backend fails
      setMessages((prev) => [
        ...prev,
        { from: 'bot', text: 'Error getting response.' }
      ]);
    }

    // Clear the input box after sending
    setInput('');
  };

  return (
    // Bootstrap container for layout, centered and padded
    <Container className="py-4" style={{ maxWidth: '800px' }}>
      <h3 className="text-center mb-4">💬 Chat with Assistant</h3>

      {/* Message display box */}
      <Card
        className="mb-3 shadow"
        style={{ height: '60vh', overflowY: 'auto', padding: '1rem' }}
      >
        {/* Loop through all messages */}
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`d-flex mb-3 ${
              msg.from === 'user' ? 'justify-content-end' : 'justify-content-start'
            }`} // Align left/right based on sender
          >
            <div
              className={`p-3 rounded text-white ${
                msg.from === 'user' ? 'bg-primary' : 'bg-secondary'
              }`} // Blue for user, grey for bot
              style={{ maxWidth: '75%' }}
            >
              {msg.text}
            </div>
          </div>
        ))}
        {/* Dummy div to scroll into view (auto-scroll) */}
        <div ref={messagesEndRef} />
      </Card>

      {/* Message input form */}
      <Form onSubmit={handleSend} className="d-flex gap-2">
        {/* Text input field */}
        <Form.Control
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        {/* Submit button */}
        <Button type="submit" variant="primary">
          Send
        </Button>
      </Form>
    </Container>
  );
}

export default Chat;
