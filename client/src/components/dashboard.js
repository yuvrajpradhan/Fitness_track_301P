import React, { useEffect, useState } from "react";
import axios from "axios";
import "../dashboard_style.css";


const Dashboard = () => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

useEffect(() => {
  const fetchData = async () => {
    try {
      const token = localStorage.getItem("accessToken");
      console.log("Token being sent:", token); // ✅ Log token to check if it exists

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
      console.error("API error:", error.response?.data); // ✅ Log actual API error response
      setError("Failed to fetch data");
      setLoading(false);
    }
  };

  fetchData();
}, []);


  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>Dashboard</h1>
      <h2>Welcome, {userData.userInfo.username}</h2>
      <h3>Personal Info</h3>
      <p>Height: {userData.userInfo.height} cm</p>
      <p>Weight: {userData.userInfo.weight} kg</p>
      <h3>Workouts</h3>
      <ul>
        {userData.workouts.map((workout) => (
          <li key={workout.id}>{workout.name} - {workout.calories_burned} kcal</li>
        ))}
      </ul>
      <h3>Goals</h3>
      <ul>
        {userData.goals.map((goal) => (
          <li key={goal.id}>{goal.goal_name}: {goal.current_value}/{goal.target_value} {goal.unit}</li>
        ))}
      </ul>
      <h3>Daily Activities</h3>
      <ul>
        {userData.dailyActivities.map((activity) => (
          <li key={activity.id}>Steps: {activity.steps}, Distance: {activity.distance} km</li>
        ))}
      </ul>
      <h3>Progress</h3>
      <ul>
        {userData.progress.map((entry) => (
          <li key={entry.id}>Weight: {entry.weight} kg, Body Fat: {entry.body_fat_percentage}%</li>
        ))}
      </ul>
      <h3>Meals</h3>
      <ul>
        {userData.meals.map((meal) => (
          <li key={meal.id}>{meal.name} - {meal.calories} kcal</li>
        ))}
      </ul>
      <h3>Water Intake</h3>
      <ul>
        {userData.waterIntake.map((water) => (
          <li key={water.id}>{water.amount} L</li>
        ))}
      </ul>
      <h3>Sleep Records</h3>
      <ul>
        {userData.sleepRecords.map((sleep) => (
          <li key={sleep.id}>Start: {sleep.sleep_start}, End: {sleep.sleep_end}, Quality: {sleep.quality_score}/10</li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
