import React, { useEffect, useState } from "react";
import "./App.scss";
import Router from "./Router";
import { ApolloClient, ApolloProvider, InMemoryCache } from "@apollo/client";

export const client = new ApolloClient({
  cache: new InMemoryCache(),
  uri: "/api/"
})

function App() {
  const [token, setToken] = useState(null);

  return (
    <ApolloProvider client={client}>
      <Router />
    </ApolloProvider>
  )
}

export default App;
