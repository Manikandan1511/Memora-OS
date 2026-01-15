import api from "./api";

// Add memory
export const addMemory = async (payload) => {
  const res = await api.post("/memory/", payload);
  return res.data;
};


// Search memories (Ask Brain)
export const searchMemory = async (query) => {
  const res = await api.post("/api/v1/memory/search", {
    query,
  });
  return res.data;
};

// Timeline
export const getTimeline = async () => {
  const res = await api.post("/api/v1/memory/timeline");
  return res.data;
};
