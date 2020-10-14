import React from "react";
import { useSelector } from "react-redux";

const Header = (props) => {
  const auth = useSelector(state => state.auth);

  return (
    <div>
      <h1>Tools.Olin</h1>
      <p>Machine shop trainings.</p>
      {
        auth.isAuthenticated
        ? (
          <div>
            Welcome, {auth.user.firstName}! <a href="/auth/logout">Logout</a>
          </div>
        ) : (
          <a href="/auth/login">Login</a>
        )
      }
    </div>
  )
}

export default Header;
