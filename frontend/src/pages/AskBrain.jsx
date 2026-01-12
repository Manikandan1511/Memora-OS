import { useState, useEffect, useRef } from "react";

export default function AskBrain() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello 👋 I am Memora Brain. Ask me anything.",
    },
  ]);
  const [input, setInput] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = () => {
    if (!input.trim()) return;

    setMessages((prev) => [
      ...prev,
      { role: "user", content: input },
      {
        role: "assistant",
        content:
          "🧠 I received your question. Backend integration is coming soon.",
      },
    ]);
    setInput("");
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
              {msg.content}
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="mt-4 flex gap-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask something..."
          className="flex-1 rounded-xl bg-slate-900 border border-slate-700 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <button
          onClick={sendMessage}
          className="px-5 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 transition"
        >
          Send
        </button>
      </div>
    </div>
  );
}
