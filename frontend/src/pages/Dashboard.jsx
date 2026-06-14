// src/pages/Dashboard.jsx
import { useEffect, useState } from "react";
import { getTasks } from "../services/taskService";
import { getUsers } from "../services/userService";
import { getProjects } from "../services/projectService";

export default function Dashboard() {
  const [summary, setSummary] = useState({
    users: 0,
    projects: 0,
    tasks: 0,
  });

  useEffect(() => {
    async function loadDashboard() {
      const [users, projects, tasks] = await Promise.all([
        getUsers(),
        getProjects(),
        getTasks(),
      ]);

      setSummary({
        users: users.length,
        projects: projects.length,
        tasks: tasks.length,
      });
    }

    loadDashboard();
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>

      <div className="card-grid">
        <div className="card">
          <h3>Total Users</h3>
          <p>{summary.users}</p>
        </div>

        <div className="card">
          <h3>Total Projects</h3>
          <p>{summary.projects}</p>
        </div>

        <div className="card">
          <h3>Total Tasks</h3>
          <p>{summary.tasks}</p>
        </div>
      </div>
    </div>
  );
}
