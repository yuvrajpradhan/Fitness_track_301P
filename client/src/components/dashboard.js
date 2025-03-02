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

  return (
    <div className="dashboard-container">
    <h1><strong>Dashboard</strong></h1>
    <h2><strong>Welcome, {userData.userInfo.username}</strong></h2>

    <div className="section">
      <h3><strong>Personal Info</strong></h3>
      <p><strong>Height:</strong> {userData.userInfo.height} cm</p>
      <p><strong>Weight:</strong> {userData.userInfo.weight} kg</p>
    </div>

    <div className="section">
      <h3><strong>Workouts</strong></h3>
      <ul>
        {userData.workouts.map((workout) => (
          <li key={workout.id}>
            <strong>Workout Name:</strong> {workout.name}<br/>
            <strong>Duration:</strong> {workout.duration} minutes<br/>
            <strong>Calories Burned:</strong> {workout.calories_burned} kcal<br/>
            <strong>Date:</strong> {workout.date}
          </li>
        ))}
      </ul>
    </div>

    <div className="section">
      <h3><strong>Goals</strong></h3>
      <ul>
        {userData.goals.map((goal) => (
          <li key={goal.id}>
            <strong>{goal.goal_name}:</strong><br/>
            <strong>Current Value:</strong> {goal.current_value} {goal.unit}<br/>
            <strong>Goal Value:</strong> {goal.target_value} {goal.unit}<br/>
            <strong>Deadline:</strong> {goal.deadline}<br/>
            <strong>Completed:</strong> {goal.completed ? "Yes" : "No"}<br/><br/>
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

    <div className="section">
      <h3><strong>Progress</strong></h3>
      <ul>
        {userData.progress.map((entry) => (
          <li key={entry.id}>
            <strong>Weight:</strong> {entry.weight} kg, <strong>Body Fat:</strong> {entry.body_fat_percentage}%<br/>
            <strong>Muscle Mass:</strong> {entry.muscle_mass} kg<br/>
            <strong>Date:</strong> {entry.date}
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
</div>



  );
};

export default Dashboard;
