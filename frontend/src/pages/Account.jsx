import { useState } from "react";
import api from "../api";
import { fidoLoginBegin, fidoLoginFinish, register, login } from "../api/auth";

export default function Account() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleFido(e) {
    e.preventDefault();
    try {
      const options = await fidoLoginBegin(email);
      const cred = await navigator.credentials.get({ publicKey: options });
      await fidoLoginFinish({
        email,
        credential_id: cred.rawId,
        client_data_json: cred.response.clientDataJSON,
        authenticator_data: cred.response.authenticatorData,
        signature: cred.response.signature,
      });
      window.location.href = "/stores";
    } catch (err) {
      setError("Security key failed");
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();

    // Attempt to register first. If the email already exists, the API will
    // return a 400 error which we ignore and then try to log in.
    try {
      await register(email, password);
    } catch (err) {
      if (!err.response || err.response.status !== 400) {
        setError("Unable to register");
        return;
      }
    }

    try {
      await login(email, password);
      window.location.href = "/stores";
    } catch {
      setError("Invalid credentials");
    }
  }

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4">
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
        <input
          className="border p-2 rounded"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && <span className="text-red-500 text-sm">{error}</span>}

        <button
          onClick={handleFido}
          className="bg-green-600 text-white py-2 rounded hover:bg-green-700"
        >
          Use Security Key
        </button>
        <button className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
          Continue with Password
        </button>
      </form>
    </div>
  );
}
