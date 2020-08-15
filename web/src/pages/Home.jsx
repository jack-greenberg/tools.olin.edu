import React, { Component } from "react";

import BasePage from "../components/page";
import { getCurrentUser } from "../services/user";

class Home extends Component {
  componentDidMount() {
    console.log(getCurrentUser());
  }
  render() {
    return (
      <BasePage>
        <p>Hello</p>
      </BasePage>
    )
  }
}

export default Home;
