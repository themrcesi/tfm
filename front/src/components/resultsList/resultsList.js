import React from "react";
import { connect } from "react-redux";
import "./resultsList.css"

export function ResultsList(props) {
  const results = ["hola", "adiós", "hola", "hola"];

  const toShow = results.map((result) => {
    return <div>{result}</div>;
  });

  return <div className="row">{toShow}</div>;
}

const mapStateToProps = (state) => {
  return {
    results: state.results,
  };
};

export default connect(mapStateToProps, null)(ResultsList);
