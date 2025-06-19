import { useState } from "react";
import api from "../api";

export default function Account() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    // Attempt to register first. If the email already exists, the API will
    // return a 400 error which we ignore and then try to log in.
    try {
      await api.post("/auth/register", { email, password });
    } catch (err) {
      if (!err.response || err.response.status !== 400) {
        setError("Unable to register");
        return;
      }
    }

    const body = new URLSearchParams();
    body.append("username", email); // field MUST be `username`
    body.append("password", password);

    try {
      const { data } = await api.post("/auth/login", body, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      localStorage.setItem("token", data.access_token);
      window.location.href = "/stores";
    } catch {
      setError("Invalid credentials");
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-4 p-8 bg-white rounded shadow w-80"
      >
        <h1 className="text-2xl font-semibold text-center">Partle Account</h1>

        <input
          className="border p-2 rounded"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="border p-2 rounded"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && <span className="text-red-500 text-sm">{error}</span>}

        <button className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
          Continue
        </button>
      </form>
    </main>
  );
}
