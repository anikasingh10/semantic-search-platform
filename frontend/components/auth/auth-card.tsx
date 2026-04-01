"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { useAuth } from "@/hooks/use-auth";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";

type AuthCardProps = {
  mode: "login" | "signup";
};

export function AuthCard({ mode }: AuthCardProps) {
  const router = useRouter();
  const { login, signup } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function formatAuthError(error: unknown): string {
    if (typeof error === "string") {
      return error;
    }

    if (Array.isArray(error)) {
      return error
        .map((item) => {
          if (typeof item === "string") {
            return item;
          }
          if (item && typeof item === "object" && "msg" in item) {
            return String(
              (item as { msg?: unknown }).msg || JSON.stringify(item),
            );
          }
          return JSON.stringify(item);
        })
        .join(" \n");
    }

    if (error && typeof error === "object") {
      if ("detail" in error) {
        return formatAuthError((error as { detail?: unknown }).detail);
      }
      return JSON.stringify(error);
    }

    return "Authentication failed.";
  }

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (mode === "signup") {
        await signup(email, password, fullName);
      } else {
        await login(email, password);
      }
      router.push("/dashboard");
    } catch (err: any) {
      setError(
        formatAuthError(
          err?.response?.data?.detail ??
            err?.message ??
            "Authentication failed.",
        ),
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="w-full max-w-md"
    >
      <Card className="bg-card/60">
        <CardHeader>
          <CardTitle className="text-2xl">
            {mode === "login" ? "Welcome back" : "Create your workspace"}
          </CardTitle>
          <CardDescription>
            {mode === "login"
              ? "Sign in to continue searching across your knowledge base."
              : "Start building your semantic knowledge engine in under a minute."}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-4" onSubmit={onSubmit}>
            {mode === "signup" ? (
              <Input
                placeholder="Full name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            ) : null}
            <Input
              placeholder="Email address"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <Input
              placeholder="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            {error ? <p className="text-sm text-red-400">{error}</p> : null}
            <Button type="submit" className="w-full" disabled={loading}>
              {loading
                ? "Please wait..."
                : mode === "login"
                  ? "Sign in"
                  : "Create account"}
            </Button>
          </form>

          <p className="mt-5 text-center text-sm text-muted-foreground">
            {mode === "login" ? "New here?" : "Already have an account?"}{" "}
            <Link
              href={mode === "login" ? "/signup" : "/login"}
              className="font-semibold text-primary hover:opacity-90"
            >
              {mode === "login" ? "Create account" : "Sign in"}
            </Link>
          </p>
        </CardContent>
      </Card>
    </motion.div>
  );
}
