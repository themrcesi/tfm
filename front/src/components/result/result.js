import React from "react";
import "./result.css";

export default function Result(props) {
  const { text, number } = props;

  return (
    <div className="result">
      <h1>Documento {number + 1}</h1>
      <p>{text}</p>
    </div>
  );
}
