// src/pages/CreateTaskPage.jsx
import { useEffect, useState } from "react";
import { getProjects } from "../services/projectService";
import { createTask } from "../services/taskService";

export default function CreateTaskPage() {
  const [projects, setProjects] = useState([]);

  const [form, setForm] = useState({
    project_id: "",
    title: "",
    description: "",
    priority: "MEDIUM",
  });

  useEffect(() => {
    async function loadProjects() {
      const data = await getProjects();
      setProjects(data);
    }

    loadProjects();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();

    await createTask({
      ...form,
      project_id: Number(form.project_id),
    });

    setForm({
      project_id: "",
      title: "",
      description: "",
      priority: "MEDIUM",
    });

    alert("Task created successfully");
  };

  return (
    <div>
      <h2>Create Task</h2>

      <form className="form" onSubmit={handleSubmit}>
        <select
          value={form.project_id}
          onChange={(e) =>
            setForm({ ...form, project_id: e.target.value })
          }
        >
          <option value="">Select Project</option>
          {projects.map((project) => (
            <option key={project.project_id} value={project.project_id}>
              {project.name}
            </option>
          ))}
        </select>

        <input
          placeholder="Task Title"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
        />

        <textarea
          placeholder="Task Description"
          value={form.description}
          onChange={(e) =>
            setForm({ ...form, description: e.target.value })
          }
        />

        <select
          value={form.priority}
          onChange={(e) =>
            setForm({ ...form, priority: e.target.value })
          }
        >
          <option value="LOW">LOW</option>
          <option value="MEDIUM">MEDIUM</option>
          <option value="HIGH">HIGH</option>
        </select>

        <button type="submit">Create Task</button>
      </form>
    </div>
  );
}
