// src/pages/TasksPage.jsx
import { useEffect, useState } from "react";
import { assignTask, getTasks, updateTaskStatus } from "../services/taskService";
import StatusBadge from "../components/StatusBadge";

export default function TasksPage() {
  const [tasks, setTasks] = useState([]);
  const [assignments, setAssignments] = useState({});
  const [statusUpdates, setStatusUpdates] = useState({});

  const loadTasks = async () => {
    const data = await getTasks();
    setTasks(data);
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleAssign = async (taskId) => {
    const userId = assignments[taskId];

    if (!userId) {
      alert("Enter user id");
      return;
    }

    await assignTask(taskId, userId);
    loadTasks();
  };

  const handleStatusUpdate = async (taskId) => {
    const newStatus = statusUpdates[taskId];

    if (!newStatus) {
      alert("Select status");
      return;
    }

    await updateTaskStatus(taskId, newStatus, "Updated from UI");
    loadTasks();
  };

  return (
    <div>
      <h2>Tasks</h2>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Project</th>
            <th>Title</th>
            <th>Status</th>
            <th>Priority</th>
            <th>Assign</th>
            <th>Status Update</th>
          </tr>
        </thead>

        <tbody>
          {tasks.map((task) => (
            <tr key={task.task_id}>
              <td>{task.task_id}</td>
              <td>{task.project_id}</td>
              <td>{task.title}</td>
              <td>
                <StatusBadge status={task.status} />
              </td>
              <td>{task.priority}</td>

              <td>
                <input
                  className="small-input"
                  placeholder="User ID"
                  value={assignments[task.task_id] || ""}
                  onChange={(e) =>
                    setAssignments({
                      ...assignments,
                      [task.task_id]: e.target.value,
                    })
                  }
                />

                <button onClick={() => handleAssign(task.task_id)}>
                  Assign
                </button>
              </td>

              <td>
                <select
                  value={statusUpdates[task.task_id] || ""}
                  onChange={(e) =>
                    setStatusUpdates({
                      ...statusUpdates,
                      [task.task_id]: e.target.value,
                    })
                  }
                >
                  <option value="">Select</option>
                  <option value="ASSIGNED">ASSIGNED</option>
                  <option value="IN_PROGRESS">IN_PROGRESS</option>
                  <option value="BLOCKED">BLOCKED</option>
                  <option value="RESOLVED">RESOLVED</option>
                  <option value="CLOSED">CLOSED</option>
                </select>

                <button onClick={() => handleStatusUpdate(task.task_id)}>
                  Update
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
