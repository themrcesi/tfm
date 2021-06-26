export const search = (language, query) => {
    return {
        type: "SEARCH",
        payload: {
            language: language,
            query: query
        }
    };
};