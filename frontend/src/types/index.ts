export interface SourceItem {
  ki_id: string;
  title: string;
  category: string | null;
  snippet: string | null;
}

export interface Message {
  id: number;
  session_id: number;
  role: "user" | "assistant";
  content: string;
  sentiment: string | null;
  frustration_score: number | null;
  sources: SourceItem[] | null;
  timestamp: string;
}

export interface ChatResponse {
  reply: string;
  sentiment: string;
  frustration_score: number;
  sources: SourceItem[];
}

export interface Session {
  session_id: string;
  user_id: string | null;
  created_at: string;
}
