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
          <a href="/auth/logout">Logout</a>
        ) : (
          <a href="/auth/login">Login</a>
        )
      }
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

export default Header;
