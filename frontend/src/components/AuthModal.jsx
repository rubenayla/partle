import { useState } from "react";

export default function AuthModal({ onClose = () => {} }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [usePassword, setUsePassword] = useState(false);

  function handleBackgroundClick(e) {
    if (e.target === e.currentTarget) onClose();
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!email) {
      setError("Enter your email");
      return;
    }
    localStorage.setItem("token", "fake_token_123");
    onClose();
  }

  return (
    <div
      onClick={handleBackgroundClick}
      className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50"
    >
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-4 bg-white rounded-3xl shadow-2xl w-full max-w-sm p-8"
      >
        <h1 className="text-2xl font-semibold text-center">Partle Account</h1>

        <input
          className="border p-2 rounded"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        {usePassword && (
          <input
            className="border p-2 rounded"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        )}

        {error && <span className="text-red-500 text-sm">{error}</span>}

        <button className="bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700">
          Continue
        </button>
        <button
          type="button"
          onClick={() => setUsePassword(!usePassword)}
          className="text-sm text-indigo-600 hover:underline"
        >
          {usePassword ? "Use passkey instead" : "Use password instead"}
        </button>
      </form>
    </div>
  );
}
