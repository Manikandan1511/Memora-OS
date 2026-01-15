import { useState, useEffect, useRef } from "react";
import { askBrain } from "../services/api";

export default function AskBrain() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello 👋 I am Memora Brain. Ask me anything.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: "user", content: input };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await askBrain(userMessage.content);

      const assistantMessage = {
        role: "assistant",
        content: response.answer,
        memories: response.memories_used || [],
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "❌ Sorry, I couldn't reach the brain right now.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-full flex flex-col">
      {/* Header */}
      <div className="mb-4">
        <h1 className="text-2xl font-semibold">Ask Brain</h1>
        <p className="text-slate-400 text-sm">
          Converse with your memory operating system
        </p>
      </div>

      {/* Chat Area */}
      <div className="flex-1 min-h-0 overflow-y-auto rounded-xl bg-slate-900 border border-slate-800 p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[70%] px-4 py-3 rounded-2xl text-sm ${
                msg.role === "user"
                  ? "bg-indigo-600 text-white rounded-br-none"
                  : "bg-slate-800 text-slate-200 rounded-bl-none"
              }`}
            >
              <p>{msg.content}</p>

              {/* Memories Used (Assistant Only) */}
              {msg.role === "assistant" &&
                msg.memories &&
                msg.memories.length > 0 && (
                  <div className="mt-3 border-t border-slate-700 pt-2 text-xs text-slate-400">
                    <p className="mb-1 font-medium">Memories used:</p>
                    <ul className="list-disc list-inside space-y-1">
                      {msg.memories.map((mem) => (
                        <li key={mem.id}>
                          {mem.content}{" "}
                          <span className="opacity-70">
                            (score: {mem.score})
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-800 text-slate-300 px-4 py-3 rounded-2xl text-sm animate-pulse">
              🧠 Thinking...
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="mt-4 flex gap-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask something..."
          disabled={loading}
          className="flex-1 rounded-xl bg-slate-900 border border-slate-700 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="px-5 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 transition disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}
