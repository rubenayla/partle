// frontend/src/components/AuthModal.tsx
import { useState, MouseEvent, FormEvent } from 'react';
import api from '../api/index.ts';
import { login, register } from '../api/auth';

interface Props {
  onClose?: () => void;
  onSuccess?: () => void;
}
export default function AuthModal({ onClose = () => { }, onSuccess = () => { } }: Props) {
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
      const response = await login(email, password);
      localStorage.setItem("token", response.access_token);
      
      // Check if user needs to set username
      if (response.needs_username) {
        window.location.href = '/complete-profile';
      } else {
        onSuccess();
      }
      onClose();
      return;
    } catch (err: any) {
      if (err?.response?.status !== 404) {
        // Show actual error from API
        const errorMessage = err?.response?.data?.detail || "Invalid credentials";
        setError(errorMessage);
        return;
      }
    }

    try {
      await register(email, password);
      const response = await login(email, password);
      localStorage.setItem("token", response.access_token);
      
      // New users always need to set username
      window.location.href = '/complete-profile';
      onClose();
    } catch (err: any) {
      // Extract error message from API response
      let errorMessage = "Registration failed";

      if (err?.response?.data?.detail) {
        // Check if it's a validation error array
        if (Array.isArray(err.response.data.detail)) {
          // Extract the first validation error message
          errorMessage = err.response.data.detail[0]?.msg || "Invalid input";
        } else {
          // Simple string error message
          errorMessage = err.response.data.detail;
        }
      }

      setError(errorMessage);
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
        className="flex flex-col gap-4 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-3xl shadow-2xl w-full max-w-sm p-8"
      >
        <h1 className="text-2xl font-semibold text-center">Partle Account Register&Login</h1>

        <input
          className="border border-gray-300 dark:border-gray-600 p-2 rounded bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
          placeholder="Email"
          autoComplete="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          className="border border-gray-300 dark:border-gray-600 p-2 rounded bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
          type="password"
          placeholder="Password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          type="button"
          onClick={handleForgot}
          className="text-sm text-blue-600 dark:text-blue-400 hover:underline text-left"
        >
          Forgot password?
        </button>

        {error && <span className="text-red-600 dark:text-red-400 text-sm">{error}</span>}

        <button className="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white py-2 rounded transition-colors">
          Continue
        </button>
      </form>
    </div>
  );
}
