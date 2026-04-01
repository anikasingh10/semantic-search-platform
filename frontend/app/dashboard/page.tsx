"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import { ChatPanel } from "@/components/dashboard/chat-panel";
import { Sidebar } from "@/components/dashboard/sidebar";
import { SourcesPanel } from "@/components/dashboard/sources-panel";
import { useAuth } from "@/hooks/use-auth";
import { apiClient } from "@/lib/api";
import type {
  Analytics,
  DocumentItem,
  HistoryItem,
  Message,
  SourceItem,
} from "@/lib/types";

export default function DashboardPage() {
  const router = useRouter();
  const { email, isAuthenticated, logout } = useAuth();

  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [selectedSources, setSelectedSources] = useState<SourceItem[]>([]);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);

  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  useEffect(() => {
    const token = localStorage.getItem("semantic_token");
    if (!token) {
      router.replace("/login");
      return;
    }

    void refreshData();
  }, [router]);

  async function refreshData() {
    const [docs, historyList, analyticsValue] = await Promise.all([
      apiClient.getDocuments(),
      apiClient.getHistory(),
      apiClient.getAnalytics(),
    ]);
    setDocuments(docs);
    setHistory(historyList);
    setAnalytics(analyticsValue);
  }

  async function handleUpload(files: File[]) {
    setUploading(true);
    setUploadProgress(0);
    try {
      await apiClient.uploadDocuments(files, setUploadProgress);
      await refreshData();
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  }

  async function handleDeleteDoc(id: string) {
    await apiClient.deleteDocument(id);
    await refreshData();
  }

  async function handleDeleteQuery(id: string) {
    await apiClient.deleteHistory(id);
    setHistory((prev) => prev.filter((item) => item.id !== id));
  }

  async function handleClearHistory() {
    if (
      confirm(
        "Are you sure you want to delete all query history? This cannot be undone.",
      )
    ) {
      await apiClient.clearAllHistory();
      setHistory([]);
    }
  }

  async function handleQuery(query: string) {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: query,
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await apiClient.chat(query);
      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: response.answer,
        sources: response.sources,
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setSelectedSources(response.sources);
      await refreshData();
    } finally {
      setLoading(false);
    }
  }

  function handleReplay(query: string) {
    void handleQuery(query);
  }

  const safeEmail = useMemo(() => email ?? null, [email]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <main className="p-4">
      <div className="grid grid-cols-1 gap-4 xl:grid-cols-[320px_minmax(0,1fr)_360px]">
        <Sidebar
          email={safeEmail}
          documents={documents}
          history={history}
          uploadProgress={uploadProgress}
          uploading={uploading}
          onFilesSelect={handleUpload}
          onDeleteDoc={handleDeleteDoc}
          onReplayQuery={handleReplay}
          onDeleteQuery={handleDeleteQuery}
          onClearHistory={handleClearHistory}
          onLogout={() => {
            logout();
            router.push("/login");
          }}
        />

        <ChatPanel
          messages={messages}
          loading={loading}
          onSubmit={handleQuery}
        />

        <SourcesPanel sources={selectedSources} analytics={analytics} />
      </div>
    </main>
  );
}
