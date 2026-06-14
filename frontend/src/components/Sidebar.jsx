//src/components/Sidebar.jsx
import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <NavLink to="/">Dashboard</NavLink>
      <NavLink to="/users">Users</NavLink>
      <NavLink to="/projects">Projects</NavLink>
      <NavLink to="/tasks">Tasks</NavLink>
      <NavLink to="/tasks/new">Create Task</NavLink>
      <NavLink to="/reports">Reports</NavLink>
    </aside>
  );
}
