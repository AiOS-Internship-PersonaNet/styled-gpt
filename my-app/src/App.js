import './App.css';
import React from 'react';

function App() {
  const [input, setInput] = React.useState(null);
  const [response, setResponse] = React.useState(null);

  async function chat() {
    console.log('User clicked submit', input);
    const body = {
      "query": input
    };

    const settings = {
      method: 'post',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    };
    const res = await fetch('/chain', settings);
    for await (const chunk of res.body) {
      setResponse(response + String.fromCharCode(chunk))
      console.log(chunk);
    }
    // fetch('/chain', settings)
    //   .then((response) => response.body)
    //   .then((body) => {
    //     const reader = body.getReader();
    //     console.log(reader)
    //   })

    //   .catch(console.log)
  };
  return (
    <div className="App">
      <header className="App-header">
        <div>
          <input
            value={input} placeholder='Input'
            onChange={e => setInput(e.target.value)} />
        </div>

        <div>
          <button onClick={chat}>submit</button>
        </div>
        <p>{response}</p>
      </header>
    </div>
  );
}

export default App;
