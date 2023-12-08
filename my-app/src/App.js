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
    const res = await fetch('/chain', settings)
    .then(function(response) {
      const body = response.body
      return body.getReader().read();
    })
    .then(function(arr) {
      const newarr = arr['value']

      var string =  new TextDecoder().decode(newarr);
      return string
    })
    console.log(res)
    setResponse(res)

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
