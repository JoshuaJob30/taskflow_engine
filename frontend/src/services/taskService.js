// src/services/taskService.js
import api from "./api";

export const getTasks = async () => {
  const response = await api.get("/tasks");
  return response.data;
};

export const getTaskById = async (taskId) => {
  const response = await api.get(`/tasks/${taskId}`);
  return response.data;
};

export const createTask = async (payload) => {
  const response = await api.post("/tasks", payload);
  return response.data;
};

export const assignTask = async (taskId, userId) => {
  const response = await api.put(`/tasks/${taskId}/assign`, {
    user_id: Number(userId),
  });
  return response.data;
};

export const updateTaskStatus = async (taskId, newStatus, changeReason) => {
  const response = await api.put(`/tasks/${taskId}/status`, {
    new_status: newStatus,
    change_reason: changeReason || null,
  });
  return response.data;
};

export const addDependency = async (taskId, dependsOnTaskId) => {
  const response = await api.post(`/tasks/${taskId}/dependencies`, {
    depends_on_task_id: Number(dependsOnTaskId),
  });
  return response.data;
};

export const getTaskDependencies = async (taskId) => {
  const response = await api.get(`/tasks/${taskId}/dependencies`);
  return response.data;
};

export const addComment = async (taskId, userId, message) => {
  const response = await api.post(`/tasks/${taskId}/comments`, {
    user_id: Number(userId),
    message,
  });
  return response.data;
};

export const getTaskHistory = async (taskId) => {
  const response = await api.get(`/tasks/${taskId}/history`);
  return response.data;
};
