import Box from "./components/searchBox/box"
import ResultsList from "./components/resultsList/resultsList"
import { useState } from "react";
import Header from "./components/header/header"

function App() {

  const [results, setResults] = useState([])

  return (
    <div className="container mt-5">
      <Header/>
      <Box setResults = {setResults}></Box>
      <ResultsList results = {results}></ResultsList>
    </div>
  );
}

export default App;
