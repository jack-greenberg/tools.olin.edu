import React from "react";
// import { compose } from "redux"
// import { connect } from "react-redux"


const Header = (props) => {
  return (
    <div>
      <h1>Tools.Olin</h1>
      <p>Machine shop trainings.</p>
      <a href="/auth/logout">Logout</a><br />
      <a href="/auth/login">Login</a>
      <h2>List of tools:</h2>
      <ul>
        <li>
          Lathe
        </li>
        <li>
          Mill
        </li>
      </ul>
    </div>
  )
}

// const withConnect = connect(
//   (state) => ({ isAuthenticated: state.auth.isAuthenticated })
// )
// 
// export default compose(
//   withConnect,
// )(Header)
export default Header;
