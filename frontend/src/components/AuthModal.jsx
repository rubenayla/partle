import { useState } from "react";
import api from "../api";
import { login, register, requestReset } from "../api/auth";


function logDebug(...args) {
  if (import.meta.env.DEV) console.debug(...args);
}

const bufToBase64 = (buf) =>
  btoa(String.fromCharCode(...new Uint8Array(buf)));

const credToJSON = (c) =>
  !c
    ? null
    : {
        id: c.id,
        type: c.type,
        rawId: bufToBase64(c.rawId),
        response: {
          clientDataJSON: bufToBase64(c.response.clientDataJSON),
          ...(c.response.attestationObject && {
            attestationObject: bufToBase64(c.response.attestationObject),
          }),
          ...(c.response.authenticatorData && {
            authenticatorData: bufToBase64(c.response.authenticatorData),
          }),
          ...(c.response.signature && {
            signature: bufToBase64(c.response.signature),
          }),
          ...(c.response.userHandle && {
            userHandle: bufToBase64(c.response.userHandle),
          }),
        },
      };

export default function AuthModal({ onClose = () => {}, onSuccess = () => {} }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [usePassword, setUsePassword] = useState(false);

  /** ─── Close when clicking backdrop ─────────────────────────── */
  const clickBackdrop = (e) => e.target === e.currentTarget && onClose();

  /** ─── Passkey flow (login then register fallback) ──────────── */
  const handlePasskey = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const { data } = await api.post("/auth/fido/login/begin", { email });
      const cred = await navigator.credentials.get({ publicKey: data });
      if (!cred) throw new Error("No credential");
      const { data: tok } = await api.post("/auth/fido/login/complete", {
        email,
        credential: credToJSON(cred),
      });
      localStorage.setItem("token", tok.access_token);
      onSuccess();
      return onClose();
    } catch (err) {
      logDebug("passkey login failed, try register", err);
    }

    try {
      const { data } = await api.post("/auth/fido/register/begin", { email });
      const cred = await navigator.credentials.create({ publicKey: data });
      if (!cred) throw new Error("Cancelled");
      const { data: tok } = await api.post("/auth/fido/register/complete", {
        email,
        credential: credToJSON(cred),
      });
      localStorage.setItem("token", tok.access_token);
      onSuccess();
      onClose();
    } catch (err) {
      logDebug("passkey register failed", err);
      setError("Passkey failed. Try password instead.");
    }
  };

  /** ─── Password flow (register if 1st time, then login) ─────── */
  const handlePassword = async (e) => {
    e.preventDefault();
    setError("");

    await register(email, password).catch(() => {});

    try {
      const { access_token } = await login(email, password);
      localStorage.setItem("token", access_token);
      onSuccess();
      onClose();
    } catch {
      setError("Invalid credentials");
    }
  };

  /** ─── “Forgot password?” handler ───────────────────────────── */
  const handleForgot = async () => {
    if (!email.includes("@")) {
      setError("Enter your e-mail above first");
      return;
    }
    try {
      await api.post("/auth/request-password-reset", { email });
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
        onSubmit={usePassword ? handlePassword : handlePasskey}
        className="flex flex-col gap-4 bg-white rounded-3xl shadow-2xl w-full max-w-sm p-8"
      >
        <h1 className="text-2xl font-semibold text-center">Partle Account</h1>

        <input
          className="border p-2 rounded"
          placeholder="Email"
          autoComplete="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        {usePassword && (
          <>
            <input
              className="border p-2 rounded"
              type="password"
              placeholder="Password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button
              type="button"
              onClick={handleForgot}
              className="text-sm text-indigo-600 hover:underline text-left"
            >
              Forgot password?
            </button>
          </>
        )}

        {error && <span className="text-red-500 text-sm">{error}</span>}

        <button className="bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700">
          {usePassword ? "Continue" : "Continue with key"}
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
