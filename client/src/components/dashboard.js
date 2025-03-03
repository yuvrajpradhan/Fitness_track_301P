import React, { useEffect, useState } from "react";
import axios from "axios";
import "../dashboard_style.css";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";
import { PieChart, Pie, Cell, Legend } from "recharts";

const Dashboard = () => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [darkMode, setDarkMode] = useState(
    localStorage.getItem("darkMode") === "enabled"
  );

  useEffect(() => {
    if (darkMode) {
      document.body.classList.add("dark-mode");
      localStorage.setItem("darkMode", "enabled");
    } else {
      document.body.classList.remove("dark-mode");
      localStorage.setItem("darkMode", "disabled");
    }
  }, [darkMode]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("accessToken");
        console.log("Token being sent:", token);

        if (!token) {
          setError("User not authenticated");
          setLoading(false);
          return;
        }

        const config = {
          headers: { Authorization: `Bearer ${token}` },
        };

        const responses = await Promise.all([
          axios.get("http://127.0.0.1:8000/api/user-dashboard/", config),
          axios.get("http://127.0.0.1:8000/api/workouts/", config),
          axios.get("http://127.0.0.1:8000/api/goals/", config),
          axios.get("http://127.0.0.1:8000/api/daily-activities/", config),
          axios.get("http://127.0.0.1:8000/api/progress/", config),
          axios.get("http://127.0.0.1:8000/api/meals/", config),
          axios.get("http://127.0.0.1:8000/api/water/", config),
          axios.get("http://127.0.0.1:8000/api/sleep/", config),
        ]);
        

        setUserData({
          userInfo: responses[0].data,
          workouts: responses[1].data,
          goals: responses[2].data,
          dailyActivities: responses[3].data,
          progress: responses[4].data,
          meals: responses[5].data,
          waterIntake: responses[6].data,
          sleepRecords: responses[7].data,
        });
        setLoading(false);
      } catch (error) {
        console.error("API error:", error.response?.data);
        setError("Failed to fetch data");
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <p className="loading-message">Loading...</p>;
  if (error) return <p className="error-message">{error}</p>;

  // Water Intake Data
  const waterData = userData.waterIntake.map((entry) => ({
    date: entry.date,
    amount: entry.amount,
  }));

  // Daily Activity Data
  const dailyActivityData = userData.dailyActivities.map((entry) => ({
    date: entry.date,
    steps: entry.steps,
    distance: entry.distance,
    calories: entry.calories_burned,
  }));

  // Macronutrient Breakdown for Pie Chart
  const processMealData = (meals) => {
    let totalCarbs = 0,
      totalProtein = 0,
      totalFat = 0;

    meals.forEach((meal) => {
      totalCarbs += meal.carbs;
      totalProtein += meal.protein;
      totalFat += meal.fat;
    });

    return [
      { name: "Carbs", value: totalCarbs },
      { name: "Protein", value: totalProtein },
      { name: "Fat", value: totalFat },
    ];
  };

  const mealData = processMealData(userData.meals);
  const COLORS = ["#FF5733", "#33FF57", "#3357FF"];

  return (
    <div className="dashboard-container">
      <div className="dashboard-grid">
        <button onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? "Light Mode" : "Dark Mode"}
        </button>
        <h1><strong>Dashboard</strong></h1>
        <h2><strong>Welcome, {userData.userInfo.username}</strong></h2>

        {/* Personal Info Section */}
        <div className="section">
          <h3><strong>Personal Info</strong></h3>
          <p><strong>Height:</strong> {userData.userInfo.height} cm</p>
          <p><strong>Weight:</strong> {userData.userInfo.weight} kg</p>
        </div>

        {/* Workouts Section */}
        <div className="section">
          <h3><strong>Workouts</strong></h3>
          <ul>
            {userData.workouts.map((workout) => (
              <li key={workout.id}>
                <strong>{workout.name}</strong> - {workout.duration} minutes, {workout.calories_burned} kcal
              </li>
            ))}
          </ul>
        </div>

        {/* Goals Section */}
        <div className="section">
          <h3><strong>Goals</strong></h3>
          <ul>
            {userData.goals.map((goal) => (
              <li key={goal.id}>
                <strong>{goal.goal_name}</strong> - {goal.current_value}/{goal.target_value} {goal.unit} 
                <br />Completed: {goal.completed ? "Yes" : "No"}
              </li>
            ))}
          </ul>
        </div>
            <div className="section">
            <h3><strong>Distance Covered</strong></h3>
            <ResponsiveContainer width="100%" height={300}>
    <LineChart data={dailyActivityData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis label={{ value: 'Km', angle: -90, position: 'insideLeft' }} />
      <Tooltip />
      <Line type="monotone" dataKey="distance" stroke="#8884d8" />
    </LineChart>
  </ResponsiveContainer>
            </div>
          <div className="section">
            <h3><strong>Daily Activity Analysis</strong></h3>
            <h4>Steps Per Day</h4>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={dailyActivityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis label={{ value: "Steps", angle: -90, position: "insideLeft" }} />
                <Tooltip formatter={(value, name, props) => [`steps: ${value}`,
                  `Date: ${props.payload.date}`]} />
                <Bar dataKey="steps" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Water Intake Analysis */}
        <div className="section">
          <h3><strong>Water Intake Analysis</strong></h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={waterData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis label={{ value: "Liters", angle: -90, position: "insideLeft" }} />
              <Tooltip />
              <Bar dataKey="amount" fill="#4A90E2" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Macronutrient Breakdown */}
        <div className="section">
          <h3><strong>Macronutrient Breakdown</strong></h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={mealData} cx="50%" cy="50%" outerRadius={100} dataKey="value" label>
                {mealData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="section">
      <h3><strong>Water Intake</strong></h3>
      <ul>
        {userData.waterIntake.map((water) => (
          <li key={water.id}>
            <strong>{water.amount} L</strong><br/>
            <strong>Date:</strong> {water.date}
          </li>
        ))}
      </ul>
    </div>
        <div className="section">
      <h3><strong>Sleep Records</strong></h3>
      <ul>
        {userData.sleepRecords.map((sleep) => (
          <li key={sleep.id}>
            <strong>Start:</strong> {sleep.sleep_start}<br/>
            <strong>End:</strong> {sleep.sleep_end}<br/>
            <strong>Quality:</strong> {sleep.quality_score}/10<br/>
            <strong>Duration:</strong> {sleep.duration} hours
          </li>
        ))}
      </ul>
    </div>
    <div className="section">
      <h3><strong>Meals</strong></h3>
      <ul>
        {userData.meals.map((meal) => (
          <li key={meal.id}>
            <strong>{meal.name}</strong> - {meal.calories} kcal<br/>
            <strong>Protein:</strong> {meal.protein}g<br/>
            <strong>Carbs:</strong> {meal.carbs}g<br/>
            <strong>Fat:</strong> {meal.fat}g<br/>
            <strong>Date:</strong> {meal.date}
          </li>
        ))}
      </ul>
    </div>
    <div className="section">
      <h3><strong>Daily Activities</strong></h3>
      <ul>
        {userData.dailyActivities.map((activity) => (
          <li key={activity.id}>
            <strong>Steps:</strong> {activity.steps}, <strong>Distance:</strong> {activity.distance} km<br/>
            <strong>Calories Burned:</strong> {activity.calories_burned} kcal<br/>
            <strong>Date:</strong> {activity.date}
          </li>
        ))}
      </ul>
    </div>
      </div>
    </div>
  );
};

export default Dashboard;
