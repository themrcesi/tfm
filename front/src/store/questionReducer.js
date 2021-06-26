const initState = {
  results: [],
};

export const questionReducer = (state = initState, action) => {
  switch (action.type) {
    case "SEARCH":
      let language = action.payload.language;
      let query = action.payload.query;

      let results = null;

      fetch(
        "http://localhost:6969/queries?query=" + query + "&language=" + language
      )
        .then((response) => response.json())
        .then((data) => {
            results = data;
        });
      return {
        ...state,
        results: results,
      };
    default:
      return state;
  }
};
export default questionReducer;
