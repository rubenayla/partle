import { useState } from "react";
import api from "../api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function submit(e) {
    e.preventDefault();
    try {
      const { data } = await api.post("/auth/login", { email, password });
      localStorage.setItem("token", data.access_token);
      window.location.href = "/stores";
    } catch (err) {
      setError("Invalid credentials");
    }
  }

  return (
    <form onSubmit={submit} className="flex flex-col gap-4 max-w-xs mx-auto">
      <input value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" />
      <button className="btn">Log in</button>
      {error && <span className="text-red-500">{error}</span>}
    </form>
  );
}
