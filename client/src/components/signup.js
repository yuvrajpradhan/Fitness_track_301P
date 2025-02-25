import React from "react";
import { Link } from "react-router-dom";

export default function Signup() {
  return (
    <div className="wrapper signUp">
      <div className="form">
        <div className="heading">CREATE AN ACCOUNT</div>
        <form>
          <div>
            <label htmlFor="name">Name</label>
            <input type="text" id="name" placeholder="Enter your name" />
          </div>
          <div>
            <label htmlFor="name">E-Mail</label>
            <input type="text" id="name" placeholder="Enter your mail" />
          </div>
          <div>
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="Enter you password"
            />
          </div>
          <div>
            <label htmlFor="name">Date of birth</label>
            <input type="date" id="name" placeholder="Enter your Date of birth" />
          </div>
          <div>
            <label htmlFor="name">Height</label>
            <input type="number" id="name" placeholder="Enter your height" />
          </div>
          <div>
            <label htmlFor="name">eight</label>
            <input type="number" id="name" placeholder="Enter you weight" />
          </div>
          <button type="submit">Submit</button>
          <h2 align="center" class="or">
            OR
          </h2>
        </form>
        <p>
          Have an account ? <Link to="/"> Login </Link>
        </p>
      </div>
    </div>
  );
}
