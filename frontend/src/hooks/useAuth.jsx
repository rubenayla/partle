// src/hooks/useAuth.js
import { useState, useEffect, createContext, useContext } from "react";
import { currentUser, login, register } from "../api/auth";

const AuthCtx = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    currentUser().then(setUser).catch(() => setUser(null));
  }, []);

  const signIn = async (email, password) => {
    await login(email, password);
    const u = await currentUser();
    setUser(u);
  };

  const value = { user, signIn, register };
  return <AuthCtx.Provider value={value}>{children}</AuthCtx.Provider>;
};

export const useAuth = () => useContext(AuthCtx);
