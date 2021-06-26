import React from "react";
import "./resultsList.css"
import Result from "../result/result"

export default function ResultsList(props) {
  const {results} = props;

  const toShow = results.map((result, key) => {
    return <Result text = {result.document} key = {key} number = {key}/>;
  });

  return <div className="row">{toShow}</div>;
}
