import React from "react";
import "./box.css";
import { useState } from "react";
import { connect } from "react-redux";
import {search} from "../../store/questionActions";

export function Box(props) {
  const [query, setQuery] = useState("");

  const handleChangeQuery = (event) => {
    setQuery(event.target.value);
  };

  const [language, setLanguage] = useState("esp");

  const handleChangeLanguage = (event) => {
    setLanguage(event.target.value);
  };

  const {search} = props

  const clickButton = () => { 
      search(language, query)
      setQuery("");
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
      <button type="submit" onClick={clickButton}>
        <i className="fa fa-search"></i>
      </button>
    </div>
  );
}

const mapDispatchToProps = (dispatch) => {
    return {
      search: (language, query) => dispatch(search(language, query)),
    };
  };

export default connect(null, mapDispatchToProps)(Box);
