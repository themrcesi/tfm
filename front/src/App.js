import Box from "./components/searchBox/box"
import ResultsList from "./components/resultsList/resultsList"
import { useState } from "react";

function App() {

  const [results, setResults] = useState([])

  return (
    <div className="container mt-5">
      <Box></Box>
      <ResultsList></ResultsList>
    </div>
  );
}

export default App;
