// src/hooks/useAuth.js
import { useState, useEffect, createContext, useContext } from "react";
import { currentUser, login, register } from "../api/auth";

const AuthCtx = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    console.log("AuthProvider: Initializing auth state");
    const token = localStorage.getItem("token");
    if (!token) {
      console.log("AuthProvider: No token found, user not logged in");
      setUser(null);
      setIsLoading(false);
      return;
    }

    console.log("AuthProvider: Token found, checking current user");
    currentUser()
      .then((userData) => {
        console.log("AuthProvider: User logged in:", userData?.email);
        setUser(userData);
      })
      .catch((error) => {
        console.log("AuthProvider: Token invalid, removing:", error.response?.status);
        localStorage.removeItem("token");
        setUser(null);
      })
      .finally(() => {
        console.log("AuthProvider: Auth initialization complete");
        setIsLoading(false);
      });
  }, []);

  const signIn = async (email, password) => {
    await login(email, password);
    const u = await currentUser();
    setUser(u);
  };

  const value = { user, signIn, register, isLoading };
  return <AuthCtx.Provider value={value}>{children}</AuthCtx.Provider>;
};

export const useAuth = () => useContext(AuthCtx);
