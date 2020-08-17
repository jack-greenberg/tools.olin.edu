import React, { Component } from "react";

class BasePage extends Component {
  render() {
    return (
      <div>
        <h1>Tools.Olin</h1>
        {this.props.children}
      </div>
    )
  }
}

export default BasePage;
