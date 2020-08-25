import React, { useEffect, useState } from "react";
import "./App.scss";
import Router from "./Router";
import axios from "axios";

const getCurrentUser = async (set) => {
  try {
    const response = await axios.post("/api/", {
      "query": `
        query getCurrentUser {
          me {
            userId
            displayName
            firstName
          }
        }
      `
    })
    set(response.data);
  } catch (error) {
    set(error.response);

    if (error.response.status === 401) {
      console.warn("User not authenticated");
    } else {
      throw new Error("Error fetching current user")
    }
  }
}

const App = () => {
  var [response, setResponse] = useState(null);

  useEffect(() => {
    getCurrentUser(setResponse);
  }, [])

  if (!response) {
    return (
      <div>
        Loading...
      </div>
    )
  }

  if (response.status === 401) {
    return (
      <div>
        <a href="/auth/login">Click here to log in.</a>
      </div>
    )
  }

  return (
    <div>
      <p>Welcome {response.data.me.firstName}</p>
    </div>
  )

  // return (
  //   <Router />
  // )
}

export default App;
