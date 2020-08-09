import React, { Component } from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";

import Home from "./pages/Home";

class AppRouter extends Component {
  render() {
    return (
      <Router>
        <Route path="/" render={() => <Home />} />
      </Router>
    );
  }
}

export default AppRouter;
