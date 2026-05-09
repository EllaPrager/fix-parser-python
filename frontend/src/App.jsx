import { useState } from "react";

function App() {

  const [fixMessage, setFixMessage] = useState("");

  return (
    <div>
      <h1>Tagora FIX Decoder</h1>

      <textarea
        rows="6"
        cols="80"
        value={fixMessage}
        onChange={(event) => setFixMessage(event.target.value)}
      />

      <p>{fixMessage}</p>
    </div>
  );
}

export default App;