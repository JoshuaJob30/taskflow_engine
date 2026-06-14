// src/pages/ProjectsPage.jsx
import { useEffect, useState } from "react";
import { createProject, getProjects } from "../services/projectService";

export default function ProjectsPage() {
  const [projects, setProjects] = useState([]);
  const [form, setForm] = useState({
    name: "",
    description: "",
  });

  const loadProjects = async () => {
    const data = await getProjects();
    setProjects(data);
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();

    await createProject(form);

    setForm({
      name: "",
      description: "",
    });

    loadProjects();
  };

  return (
    <div>
      <h2>Projects</h2>

      <form className="form" onSubmit={handleSubmit}>
        <input
          placeholder="Project Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />

        <input
          placeholder="Description"
          value={form.description}
          onChange={(e) =>
            setForm({ ...form, description: e.target.value })
          }
        />

        <button type="submit">Create Project</button>
      </form>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Project</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {projects.map((project) => (
            <tr key={project.project_id}>
              <td>{project.project_id}</td>
              <td>{project.name}</td>
              <td>{project.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
