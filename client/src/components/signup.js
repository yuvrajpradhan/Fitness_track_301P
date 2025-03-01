import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

export default function Signup() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    date_of_birth: "",
    height: "",
    weight: "",
  });

  const [error, setError] = useState(""); // Ensure this is used in JSX
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/signup/", formData,
        { headers: { "Content-Type": "application/json" }
       ,}
      );

      if (response.status === 201) {
        alert("Account created successfully! Please log in.");
        navigate("/");
      }
    } catch (err) {
      setError(err.response?.data?.error || "Signup failed. Please try again.");
    }
  };

  return (
    <div className="wrapper signUp">
      <div className="form">
        <div className="heading">CREATE AN ACCOUNT</div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <form onSubmit={handleSignup}>
          <div>
            <label htmlFor="username">Name</label>
            <input type="text" id="username" name="username" placeholder="Enter your name" onChange={handleChange} required />
          </div>
          <div>
            <label htmlFor="email">E-Mail</label>
            <input type="email" id="email" name="email" placeholder="Enter your email" onChange={handleChange} required />
          </div>
          <div>
            <label htmlFor="password">Password</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" onChange={handleChange} required />
          </div>
          <div>
            <label htmlFor="date_of_birth">Date of Birth</label>
            <input type="date" id="date_of_birth" name="date_of_birth" onChange={handleChange} required />
          </div>
          <div>
            <label htmlFor="height">Height (cm)</label>
            <input type="number" id="height" name="height" placeholder="Enter your height" onChange={handleChange} required />
          </div>
          <div>
            <label htmlFor="weight">Weight (kg)</label>
            <input type="number" id="weight" name="weight" placeholder="Enter your weight" onChange={handleChange} required />
          </div>
          <button type="submit">Sign Up</button>
        </form>
        <p>
          Have an account? <Link to="/">Login</Link>
        </p>
      </div>
    </div>
  );
}
