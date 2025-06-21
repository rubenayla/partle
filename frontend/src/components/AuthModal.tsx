// frontend/src/components/AuthModal.tsx
import { useState, MouseEvent, FormEvent } from 'react';
import api from '../api/index.js';
import { login, register } from '../api/auth';

interface Props {
  onClose?: () => void;
  onSuccess?: () => void;
}
export default function AuthModal({ onClose = () => {}, onSuccess = () => {} }: Props) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const clickBackdrop = (e: MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) onClose();
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      const { access_token } = await login(email, password);
      localStorage.setItem("token", access_token);
      onSuccess();
      onClose();
      return;
    } catch (err) {
      if (err?.response?.status !== 404) {
        setError("Invalid credentials");
        return;
      }
    }

    try {
      await register(email, password);
      const { access_token } = await login(email, password);
      localStorage.setItem("token", access_token);
      onSuccess();
      onClose();
    } catch {
      setError("Existing account – log in instead");
    }
  };

  const handleForgot = async () => {
    if (!email.includes("@")) {
      setError("Enter your e-mail above first");
      return;
    }
    try {
      await api.post("/v1/auth/request-password-reset", { email });
      alert("Check your inbox for a reset link.");
    } catch {
      alert("Could not send reset e-mail.");
    }
  };

  return (
    <div
      onClick={clickBackdrop}
      className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50"
    >
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-4 bg-surface text-foreground rounded-3xl shadow-2xl w-full max-w-sm p-8"
      >
        <h1 className="text-2xl font-semibold text-center">Partle Account (Register/Login)</h1>

        <input
          className="border border-gray-300 dark:border-gray-600 p-2 rounded bg-background"
          placeholder="Email"
          autoComplete="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          className="border border-gray-300 dark:border-gray-600 p-2 rounded bg-background"
          type="password"
          placeholder="Password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          type="button"
          onClick={handleForgot}
          className="text-sm text-link hover:underline text-left"
        >
          Forgot password?
        </button>

        {error && <span className="text-danger text-sm">{error}</span>}

        <button className="bg-accent text-background py-2 rounded hover:bg-accent-hover">
          Continue
        </button>
      </form>
    </div>
  );
}
