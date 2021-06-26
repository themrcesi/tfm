import { createStore, applyMiddleware } from "redux";
import questionReducer from "./store/questionReducer";
import thunk from "redux-thunk";

export const middlewares = [
  thunk,
];

export const middlewaresForTesting = [
  thunk,
];

export const createStoreWithMiddleware = applyMiddleware(...middlewares)(
  createStore
);

export const store = createStoreWithMiddleware(questionReducer);