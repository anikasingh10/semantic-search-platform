"use client";

import { motion } from "framer-motion";
import { FileText, LogOut, Plus, Trash2 } from "lucide-react";

import type { DocumentItem, HistoryItem } from "@/lib/types";
import { formatDate } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";

type SidebarProps = {
  email: string | null;
  documents: DocumentItem[];
  history: HistoryItem[];
  uploadProgress: number;
  uploading: boolean;
  onFilesSelect: (files: File[]) => void;
  onDeleteDoc: (id: string) => void;
  onReplayQuery: (query: string) => void;
  onDeleteQuery: (id: string) => void;
  onClearHistory: () => void;
  onLogout: () => void;
};

export function Sidebar({
  email,
  documents,
  history,
  uploadProgress,
  uploading,
  onFilesSelect,
  onDeleteDoc,
  onReplayQuery,
  onDeleteQuery,
  onClearHistory,
  onLogout,
}: SidebarProps) {
  return (
    <Card className="flex h-[calc(100vh-2rem)] flex-col p-4">
      <div className="flex items-center justify-between gap-2">
        <div>
          <p className="text-xs text-muted-foreground">Workspace</p>
          <p className="text-sm font-semibold">{email ?? "Signed in user"}</p>
        </div>
        <Button variant="ghost" size="icon" onClick={onLogout}>
          <LogOut className="h-4 w-4" />
        </Button>
      </div>

      <Separator className="my-4" />

      <label className="block">
        <input
          type="file"
          multiple
          accept=".pdf"
          className="hidden"
          onChange={(e) => {
            if (!e.target.files?.length) {
              return;
            }
            onFilesSelect(Array.from(e.target.files));
            e.currentTarget.value = "";
          }}
        />
        <Button className="w-full gap-2" asChild>
          <span>
            <Plus className="h-4 w-4" />
            Upload PDFs
          </span>
        </Button>
      </label>

      {uploading ? (
        <div className="mt-3 space-y-2">
          <p className="text-xs text-muted-foreground">
            Uploading and indexing...
          </p>
          <Progress value={uploadProgress} />
        </div>
      ) : null}

      <div className="mt-5">
        <div className="mb-2 flex items-center justify-between">
          <p className="text-sm font-semibold">Documents</p>
          <Badge variant="secondary">{documents.length}</Badge>
        </div>
        <ScrollArea className="h-52">
          <div className="space-y-2 pr-2">
            {documents.map((doc) => (
              <motion.div
                key={doc.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className="rounded-2xl border border-border/60 bg-card/50 p-3"
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium">{doc.name}</p>
                    <p className="text-xs text-muted-foreground">
                      {doc.page_count} pages • {doc.chunk_count} chunks
                    </p>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => onDeleteDoc(doc.id)}
                    className="h-8 w-8"
                  >
                    <Trash2 className="h-3.5 w-3.5 text-red-300" />
                  </Button>
                </div>
              </motion.div>
            ))}
            {!documents.length ? (
              <div className="rounded-2xl border border-dashed border-border p-4 text-center text-xs text-muted-foreground">
                No documents yet.
              </div>
            ) : null}
          </div>
        </ScrollArea>
      </div>

      <Separator className="my-4" />

      <div className="flex-1">
        <div className="mb-2 flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <FileText className="h-4 w-4 text-muted-foreground" />
            <p className="text-sm font-semibold">Query History</p>
          </div>
          {history.length > 0 ? (
            <Button
              variant="ghost"
              size="sm"
              onClick={onClearHistory}
              className="h-6 px-2 text-xs text-red-400 hover:text-red-500"
            >
              Clear
            </Button>
          ) : null}
        </div>
        <ScrollArea className="h-[calc(100%-2rem)]">
          <div className="space-y-2 pr-2">
            {history.map((item) => (
              <div
                key={item.id}
                className="group rounded-2xl border border-border/60 bg-card/40 p-3"
              >
                <button
                  type="button"
                  onClick={() => onReplayQuery(item.query)}
                  className="w-full text-left transition hover:opacity-80"
                >
                  <p className="line-clamp-2 text-sm">{item.query}</p>
                  <p className="mt-1 text-xs text-muted-foreground">
                    {formatDate(item.created_at)}
                  </p>
                </button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => onDeleteQuery(item.id)}
                  className="mt-2 h-6 w-6 opacity-0 transition group-hover:opacity-100"
                >
                  <Trash2 className="h-3 w-3 text-red-300" />
                </Button>
              </div>
            ))}
            {!history.length ? (
              <p className="text-xs text-muted-foreground">
                No past queries yet.
              </p>
            ) : null}
          </div>
        </ScrollArea>
      </div>
    </Card>
  );
}
