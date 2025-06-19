import { useState } from "react";
import api from "../api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const { data } = await api.post("/auth/login", {
        username: email,          // OAuth2PasswordRequestForm expects these keys
        password,
      });
      localStorage.setItem("token", data.access_token);
      window.location.href = "/stores";
    } catch {
      setError("Invalid credentials");
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 p-8 bg-white rounded shadow w-80">
        <h1 className="text-2xl font-semibold text-center">Partle Login</h1>

        <input
          className="border p-2 rounded"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
        <input
          className="border p-2 rounded"
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />

        {error && <span className="text-red-500 text-sm">{error}</span>}

        <button className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
          Log in
        </button>
      </form>
    </main>
  );
}
