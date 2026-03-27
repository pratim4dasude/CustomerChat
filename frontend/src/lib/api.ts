import { ChatResponse, Message, Session } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function createSession(userId?: string): Promise<Session> {
  const response = await fetch(`${API_BASE_URL}/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId }),
  });

  if (!response.ok) {
    throw new Error("Failed to create session");
  }

  return response.json();
}

export async function getMessages(sessionId: string): Promise<{ messages: Message[] }> {
  const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}/messages`);

  if (!response.ok) {
    throw new Error("Failed to fetch messages");
  }

  return response.json();
}

export async function sendMessage(
  sessionId: string,
  content: string,
  userId?: string
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content, user_id: userId }),
  });

  if (!response.ok) {
    throw new Error("Failed to send message");
  }

  return response.json();
}
