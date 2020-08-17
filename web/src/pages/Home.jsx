import React from "react";
// import { useQuery } from "@apollo/client";
import axios from "axios";

import BasePage from "../components/page";
// import { userQuery } from "../services/user";

const Home = () => {
  axios.post("/api/", {
    "query": `
      query whoami {
        me {
          display_name
          user_id
        }
      }
    `
  })
    .then(response => {
      console.log(response.data)
    })
    .catch(err => {
      console.log(err.response.data.login_url);
      // return (
      //   <BasePage>
      //     <h1>Login Here</h1>
      //     <a href="{err.response.data.login_url}">Microsoft</a>
      //   </BasePage>
      // )
    })

  return (
    <BasePage>
      <p>Called</p>
    </BasePage>
  )
}

export default Home;
