import React from "react";
import axios from "axios";
import { useState } from "react";
import "./style.css";
import Login from "./components/login";
import Signup from "./components/signup";
import Error from "./components/error";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";


function App() {
  
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="*" element={<Error />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
