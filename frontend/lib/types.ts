export type AuthResponse = {
  access_token: string;
  token_type: string;
  user_id: string;
  email: string;
};

export type DocumentItem = {
  id: string;
  name: string;
  created_at: string;
  page_count: number;
  chunk_count: number;
};

export type SourceItem = {
  text: string;
  score: number;
  document_name: string;
  page_number: number;
};

export type ChatResponse = {
  answer: string;
  sources: SourceItem[];
};

export type HistoryItem = {
  id: string;
  query: string;
  response?: string;
  created_at: string;
};

export type Analytics = {
  document_count: number;
  query_count: number;
};

export type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: SourceItem[];
};
