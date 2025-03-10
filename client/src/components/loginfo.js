import React, { useState } from "react";
import axios from "axios";

const Loginfo = () => {
  const [workout, setWorkout] = useState({ name: "", duration: "", caloriesBurned: "" });
  const [goal, setGoal] = useState({ goalName: "", targetValue: "", unit: "" });
  const [meal, setMeal] = useState({ name: "", calories: "", protein: "", carbs: "", fat: "", date: "" });
  const [water, setWater] = useState({ amount: "", date: "" });
  const [sleep, setSleep] = useState({ sleepStart: "", sleepEnd: "", qualityScore: "", duration: "" });
  const [activity, setActivity] = useState({ steps: "", distance: "", caloriesBurned: "", date: "" });

  // Get the JWT token from localStorage or wherever it's stored
  const token = localStorage.getItem("token");
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  // Handler for workout form input changes
  const handleWorkoutChange = (e) => {
    const { name, value } = e.target;
    setWorkout({ ...workout, [name]: value });
  };

  // Handler for goal form input changes
  const handleGoalChange = (e) => {
    const { name, value } = e.target;
    setGoal({ ...goal, [name]: value });
  };

  // Handler for meal form input changes
  const handleMealChange = (e) => {
    const { name, value } = e.target;
    setMeal({ ...meal, [name]: value });
  };

  // Handler for water form input changes
  const handleWaterChange = (e) => {
    const { name, value } = e.target;
    setWater({ ...water, [name]: value });
  };

  // Handler for sleep form input changes
  const handleSleepChange = (e) => {
    const { name, value } = e.target;
    setSleep({ ...sleep, [name]: value });
  };

  // Handler for activity form input changes
  const handleActivityChange = (e) => {
    const { name, value } = e.target;
    setActivity({ ...activity, [name]: value });
  };

  // Submit handlers for each form
  const handleWorkoutSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/workouts/", workout, config);
      console.log("Workout logged:", response.data);
      alert("Workout logged successfully!");
    } catch (error) {
      console.error("Error logging workout:", error);
      alert("Failed to log workout.");
    }
  };

  const handleGoalSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/goals/", goal, config);
      console.log("Goal logged:", response.data);
      alert("Goal logged successfully!");
    } catch (error) {
      console.error("Error logging goal:", error);
      alert("Failed to log goal.");
    }
  };

  const handleMealSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/meals/", meal, config);
      console.log("Meal logged:", response.data);
      alert("Meal logged successfully!");
    } catch (error) {
      console.error("Error logging meal:", error);
      alert("Failed to log meal.");
    }
  };

  const handleWaterSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/water/", water, config);
      console.log("Water intake logged:", response.data);
      alert("Water intake logged successfully!");
    } catch (error) {
      console.error("Error logging water intake:", error);
      alert("Failed to log water intake.");
    }
  };

  const handleSleepSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/sleep/", sleep, config);
      console.log("Sleep logged:", response.data);
      alert("Sleep logged successfully!");
    } catch (error) {
      console.error("Error logging sleep:", error);
      alert("Failed to log sleep.");
    }
  };

  const handleActivitySubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/daily-activities/", activity, config);
      console.log("Activity logged:", response.data);
      alert("Activity logged successfully!");
    } catch (error) {
      console.error("Error logging activity:", error);
      alert("Failed to log activity.");
    }
  };

  return (
    <div className="loginfo-container">
      <h1>Log Information</h1>

      {/* Workout Form */}
      <form onSubmit={handleWorkoutSubmit}>
        <h2>Log Workout</h2>
        <input
          type="text"
          name="name"
          placeholder="Workout Name"
          value={workout.name}
          onChange={handleWorkoutChange}
          required
        />
        <input
          type="number"
          name="duration"
          placeholder="Duration (minutes)"
          value={workout.duration}
          onChange={handleWorkoutChange}
          required
        />
        <input
          type="number"
          name="caloriesBurned"
          placeholder="Calories Burned"
          value={workout.caloriesBurned}
          onChange={handleWorkoutChange}
          required
        />
        <button type="submit">Log Workout</button>
      </form>

      {/* Goal Form */}
      <form onSubmit={handleGoalSubmit}>
        <h2>Log Goal</h2>
        <input
          type="text"
          name="goalName"
          placeholder="Goal Name"
          value={goal.goalName}
          onChange={handleGoalChange}
          required
        />
        <input
          type="number"
          name="targetValue"
          placeholder="Target Value"
          value={goal.targetValue}
          onChange={handleGoalChange}
          required
        />
        <input
          type="text"
          name="unit"
          placeholder="Unit"
          value={goal.unit}
          onChange={handleGoalChange}
          required
        />
        <button type="submit">Log Goal</button>
      </form>

      {/* Meal Form */}
      <form onSubmit={handleMealSubmit}>
        <h2>Log Meal</h2>
        <input
          type="text"
          name="name"
          placeholder="Meal Name"
          value={meal.name}
          onChange={handleMealChange}
          required
        />
        <input
          type="number"
          name="calories"
          placeholder="Calories"
          value={meal.calories}
          onChange={handleMealChange}
          required
        />
        <input
          type="number"
          name="protein"
          placeholder="Protein (g)"
          value={meal.protein}
          onChange={handleMealChange}
          required
        />
        <input
          type="number"
          name="carbs"
          placeholder="Carbs (g)"
          value={meal.carbs}
          onChange={handleMealChange}
          required
        />
        <input
          type="number"
          name="fat"
          placeholder="Fat (g)"
          value={meal.fat}
          onChange={handleMealChange}
          required
        />
        <input
          type="date"
          name="date"
          value={meal.date}
          onChange={handleMealChange}
          required
        />
        <button type="submit">Log Meal</button>
      </form>

      {/* Water Intake Form */}
      <form onSubmit={handleWaterSubmit}>
        <h2>Log Water Intake</h2>
        <input
          type="number"
          name="amount"
          placeholder="Amount (L)"
          value={water.amount}
          onChange={handleWaterChange}
          required
        />
        <input
          type="date"
          name="date"
          value={water.date}
          onChange={handleWaterChange}
          required
        />
        <button type="submit">Log Water Intake</button>
      </form>

      {/* Sleep Form */}
      <form onSubmit={handleSleepSubmit}>
        <h2>Log Sleep</h2>
        <input
          type="datetime-local"
          name="sleepStart"
          placeholder="Sleep Start"
          value={sleep.sleepStart}
          onChange={handleSleepChange}
          required
        />
        <input
          type="datetime-local"
          name="sleepEnd"
          placeholder="Sleep End"
          value={sleep.sleepEnd}
          onChange={handleSleepChange}
          required
        />
        <input
          type="number"
          name="qualityScore"
          placeholder="Quality Score (1-10)"
          value={sleep.qualityScore}
          onChange={handleSleepChange}
          required
        />
        <input
          type="number"
          name="duration"
          placeholder="Duration (hours)"
          value={sleep.duration}
          onChange={handleSleepChange}
          required
        />
        <button type="submit">Log Sleep</button>
      </form>

      {/* Daily Activity Form */}
      <form onSubmit={handleActivitySubmit}>
        <h2>Log Daily Activity</h2>
        <input
          type="number"
          name="steps"
          placeholder="Steps"
          value={activity.steps}
          onChange={handleActivityChange}
          required
        />
        <input
          type="number"
          name="distance"
          placeholder="Distance (km)"
          value={activity.distance}
          onChange={handleActivityChange}
          required
        />
        <input
          type="number"
          name="caloriesBurned"
          placeholder="Calories Burned"
          value={activity.caloriesBurned}
          onChange={handleActivityChange}
          required
        />
        <input
          type="date"
          name="date"
          value={activity.date}
          onChange={handleActivityChange}
          required
        />
        <button type="submit">Log Activity</button>
      </form>
    </div>
  );
};

export default Loginfo;