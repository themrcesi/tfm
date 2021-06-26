import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { Provider } from "react-redux";
import { store } from "./createStore";

const myStore = store;

ReactDOM.render(
    <Provider store={myStore}>
      <App />
    </Provider>,
  document.getElementById('root')
);

