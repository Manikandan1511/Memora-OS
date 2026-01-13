import { useState } from "react";
import {
  addMemory,
  searchMemory,
  getTimeline,
} from "../services/memoryService";

export default function useMemory() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const createMemory = async (text) => {
    try {
      setLoading(true);
      return await addMemory({ content: text });
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  const askBrain = async (query) => {
    try {
      setLoading(true);
      return await searchMemory(query);
    } finally {
      setLoading(false);
    }
  };

  const timeline = async () => {
    return await getTimeline();
  };

  return {
    createMemory,
    askBrain,
    timeline,
    loading,
    error,
  };
}
