// src/pages/UsersPage.jsx
import { useEffect, useState } from "react";
import { createUser, getUsers } from "../services/userService";

export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({
    name: "",
    email: "",
    role: "USER",
    max_active_tasks: 3,
  });

  const loadUsers = async () => {
    const data = await getUsers();
    setUsers(data);
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();

    await createUser({
      ...form,
      max_active_tasks: Number(form.max_active_tasks),
    });

    setForm({
      name: "",
      email: "",
      role: "USER",
      max_active_tasks: 3,
    });

    loadUsers();
  };

  return (
    <div>
      <h2>Users</h2>

      <form className="form" onSubmit={handleSubmit}>
        <input
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />

        <input
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />

        <select
          value={form.role}
          onChange={(e) => setForm({ ...form, role: e.target.value })}
        >
          <option value="USER">USER</option>
          <option value="ADMIN">ADMIN</option>
        </select>

        <input
          type="number"
          placeholder="Max Active Tasks"
          value={form.max_active_tasks}
          onChange={(e) =>
            setForm({ ...form, max_active_tasks: e.target.value })
          }
        />

        <button type="submit">Create User</button>
      </form>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Max Active</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.user_id}>
              <td>{user.user_id}</td>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>{user.role}</td>
              <td>{user.max_active_tasks}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
