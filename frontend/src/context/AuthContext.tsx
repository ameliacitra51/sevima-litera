import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { authService } from '@/services/auth';
import type { LoginPayload, RegisterPayload, User } from '@/types/catalog';

interface AuthContextValue {
  user: User | null;
  isLoading: boolean;
  login: (payload: LoginPayload) => Promise<User>;
  register: (payload: RegisterPayload) => Promise<User>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider: React.FC<React.PropsWithChildren> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(authService.hasToken());

  useEffect(() => {
    if (!authService.hasToken()) return;
    authService.me()
      .then(setUser)
      .catch(() => {
        authService.clearToken();
        setUser(null);
      })
      .finally(() => setIsLoading(false));
  }, []);

  const value = useMemo<AuthContextValue>(() => ({
    user,
    isLoading,
    login: async (payload) => {
      const result = await authService.login(payload);
      setUser(result.user);
      return result.user;
    },
    register: async (payload) => {
      const result = await authService.register(payload);
      return result;
    },
    logout: async () => {
      await authService.logout().catch(() => undefined);
      setUser(null);
    },
  }), [isLoading, user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used inside AuthProvider');
  return context;
};
