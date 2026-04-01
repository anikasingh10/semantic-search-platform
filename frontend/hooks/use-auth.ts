'use client';

import { useEffect, useMemo, useState } from 'react';

import { apiClient } from '@/lib/api';

export function useAuth() {
  const [token, setToken] = useState<string | null>(null);
  const [email, setEmail] = useState<string | null>(null);

  useEffect(() => {
    setToken(localStorage.getItem('semantic_token'));
    setEmail(localStorage.getItem('semantic_email'));
  }, []);

  const isAuthenticated = useMemo(() => Boolean(token), [token]);

  function persistAuth(nextToken: string, nextEmail: string) {
    localStorage.setItem('semantic_token', nextToken);
    localStorage.setItem('semantic_email', nextEmail);
    setToken(nextToken);
    setEmail(nextEmail);
  }

  async function login(emailValue: string, password: string) {
    const auth = await apiClient.login(emailValue, password);
    persistAuth(auth.access_token, auth.email);
  }

  async function signup(emailValue: string, password: string, fullName?: string) {
    const auth = await apiClient.signup(emailValue, password, fullName);
    persistAuth(auth.access_token, auth.email);
  }

  function logout() {
    localStorage.removeItem('semantic_token');
    localStorage.removeItem('semantic_email');
    setToken(null);
    setEmail(null);
  }

  return {
    token,
    email,
    isAuthenticated,
    login,
    signup,
    logout,
  };
}
