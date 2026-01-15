// frontend/src/services/api.js

import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

   // ASK BRAIN API

export const askBrain = async (question) => {
  const response = await api.post("/brain/ask", {
    question,
  });

  return response.data;
};

export default api;
