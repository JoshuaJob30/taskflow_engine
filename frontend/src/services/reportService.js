// src/services/reportService.js
import api from "./api";

export const getWorkloadReport = async () => {
  const response = await api.get("/reports/workload");
  return response.data;
};

export const getProjectProgressReport = async () => {
  const response = await api.get("/reports/project-progress");
  return response.data;
};

export const getBlockedTasksReport = async () => {
  const response = await api.get("/reports/blocked-tasks");
  return response.data;
};
