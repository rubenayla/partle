// src/hooks/useAuth.js
import { useState, useEffect, createContext, useContext } from "react";
import {
  currentUser,
  login,
  register,
  fidoLoginBegin,
  fidoLoginFinish,
  fidoRegisterBegin,
  fidoRegisterFinish,
} from "../api/auth";

const AuthCtx = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    currentUser()
      .then(setUser)
      .catch(() => setUser(null));
  }, []);

  const signIn = async (email, password) => {
    await login(email, password);
    const u = await currentUser();
    setUser(u);
  };

  const signInWithFido = async (email) => {
    const optionsHex = await fidoLoginBegin(email);
    const options = CBOR.decode(Buffer.from(optionsHex, "hex"));
    const cred = await navigator.credentials.get({ publicKey: options });
    const result = await fidoLoginFinish({
      email,
      credential_id: new Uint8Array(cred.rawId),
      client_data_json: new Uint8Array(cred.response.clientDataJSON),
      authenticator_data: new Uint8Array(cred.response.authenticatorData),
      signature: new Uint8Array(cred.response.signature),
    });
    const u = await currentUser();
    setUser(u);
    return result;
  };

  const registerFido = async () => {
    const optionsHex = await fidoRegisterBegin();
    const options = CBOR.decode(Buffer.from(optionsHex, "hex"));
    const cred = await navigator.credentials.create({ publicKey: options });
    await fidoRegisterFinish({
      client_data_json: new Uint8Array(cred.response.clientDataJSON),
      attestation_object: new Uint8Array(cred.response.attestationObject),
    });
  };

  const value = { user, signIn, signInWithFido, register, registerFido };
  return <AuthCtx.Provider value={value}>{children}</AuthCtx.Provider>;
};

export const useAuth = () => useContext(AuthCtx);
