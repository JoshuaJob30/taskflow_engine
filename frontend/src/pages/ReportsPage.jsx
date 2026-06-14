// src/pages/ReportsPage.jsx
import { useEffect, useState } from "react";
import {
  getBlockedTasksReport,
  getProjectProgressReport,
  getWorkloadReport,
} from "../services/reportService";

export default function ReportsPage() {
  const [workload, setWorkload] = useState([]);
  const [progress, setProgress] = useState([]);
  const [blocked, setBlocked] = useState([]);

  useEffect(() => {
    async function loadReports() {
      const [workloadData, progressData, blockedData] = await Promise.all([
        getWorkloadReport(),
        getProjectProgressReport(),
        getBlockedTasksReport(),
      ]);

      setWorkload(workloadData);
      setProgress(progressData);
      setBlocked(blockedData);
    }

    loadReports();
  }, []);

  return (
    <div>
      <h2>Reports</h2>

      <section>
        <h3>User Workload</h3>
        <table>
          <thead>
            <tr>
              <th>User ID</th>
              <th>User</th>
              <th>Active Tasks</th>
            </tr>
          </thead>
          <tbody>
            {workload.map((row) => (
              <tr key={row.user_id}>
                <td>{row.user_id}</td>
                <td>{row.user_name}</td>
                <td>{row.active_task_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section>
        <h3>Project Progress</h3>
        <table>
          <thead>
            <tr>
              <th>Project</th>
              <th>Total</th>
              <th>Closed</th>
              <th>Completion %</th>
            </tr>
          </thead>
          <tbody>
            {progress.map((row) => (
              <tr key={row.project_id}>
                <td>{row.project_name}</td>
                <td>{row.total_tasks}</td>
                <td>{row.closed_tasks}</td>
                <td>{row.completion_percentage}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section>
        <h3>Blocked Tasks</h3>
        <table>
          <thead>
            <tr>
              <th>Task</th>
              <th>Status</th>
              <th>Blocking Task</th>
              <th>Blocking Status</th>
            </tr>
          </thead>
          <tbody>
            {blocked.map((row) => (
              <tr key={row.task_id}>
                <td>{row.title}</td>
                <td>{row.status}</td>
                <td>{row.blocking_task_id}</td>
                <td>{row.blocking_task_status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
