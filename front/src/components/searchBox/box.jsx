import React from "react";
import "./box.css";
import { useState } from "react";

export default function Box(props) {
  const [query, setQuery] = useState("");

  const {setResults} = props;

  const handleChangeQuery = (event) => {
    setQuery(event.target.value);
  };

  const [language, setLanguage] = useState("esp");

  const handleChangeLanguage = (event) => {
    setLanguage(event.target.value);
  };

  const search = () => {
    fetch("http://localhost:6969/queries?query="+query+"&language="+language)
    .then(response => response.json())
    .then(data => {
      setResults(data);
      /*setQuery("");*/
    });
  };

  return (
    <div className="search-box">
      <input
        type="text"
        placeholder="Search.."
        name="search"
        value={query}
        onChange={handleChangeQuery}
      />
      <select value={language} onChange={handleChangeLanguage} name="language">
        <option value="eng">Inglés</option>
        <option value="esp" selected>
          Español
        </option>
      </select>
      <button type="submit" onClick = {search}>
        <i className="fa fa-search"></i>
      </button>
    </div>
  );
}
