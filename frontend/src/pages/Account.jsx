import { useState } from "react";
import api from "../api";

function bufToBase64(buf) {
  return btoa(String.fromCharCode(...new Uint8Array(buf)));
}

function credToJSON(cred) {
  if (!cred) return null;
  const json = {
    id: cred.id,
    type: cred.type,
    rawId: bufToBase64(cred.rawId),
    response: {
      clientDataJSON: bufToBase64(cred.response.clientDataJSON),
    },
  };
  if (cred.response.attestationObject)
    json.response.attestationObject = bufToBase64(cred.response.attestationObject);
  if (cred.response.authenticatorData)
    json.response.authenticatorData = bufToBase64(cred.response.authenticatorData);
  if (cred.response.signature)
    json.response.signature = bufToBase64(cred.response.signature);
  if (cred.response.userHandle)
    json.response.userHandle = bufToBase64(cred.response.userHandle);
  return json;
}

export default function Account() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [usePassword, setUsePassword] = useState(false);

  async function handlePasskey(e) {
    e.preventDefault();
    setError("");
    try {
      const { data } = await api.post("/auth/fido/login/begin", { email });
      const cred = await navigator.credentials.get({ publicKey: data });
      const { data: token } = await api.post("/auth/fido/login/complete", {
        email,
        credential: credToJSON(cred),
      });
      localStorage.setItem("token", token.access_token);
      window.location.href = "/stores";
      return;
    } catch {}

    try {
      const { data } = await api.post("/auth/fido/register/begin", { email });
      const cred = await navigator.credentials.create({ publicKey: data });
      const { data: token } = await api.post("/auth/fido/register/complete", {
        email,
        credential: credToJSON(cred),
      });
      localStorage.setItem("token", token.access_token);
      window.location.href = "/stores";
    } catch {
      setError("Passkey failed");
    }
  }

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
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4">
      <form
        onSubmit={usePassword ? handleSubmit : handlePasskey}
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
