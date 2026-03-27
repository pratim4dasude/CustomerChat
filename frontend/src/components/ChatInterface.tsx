"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { Message, SourceItem } from "@/types";
import { createSession, getMessages, sendMessage } from "@/lib/api";
import { ChatBubble } from "./ChatBubble";
import { SentimentPanel } from "./SentimentPanel";
import { SourcesPanel } from "./SourcesPanel";
import { Bot, Send, Loader2, Circle } from "lucide-react";
import Link from "next/link";

export function ChatInterface() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);
  const [currentSentiment, setCurrentSentiment] = useState<string | null>(null);
  const [currentFrustration, setCurrentFrustration] = useState<number | null>(null);
  const [currentSources, setCurrentSources] = useState<SourceItem[] | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    async function initSession() {
      try {
        const session = await createSession();
        setSessionId(session.session_id);
        setIsInitialized(true);
      } catch (error) {
        console.error("Failed to create session:", error);
      }
    }
    initSession();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = useCallback(async () => {
    if (!inputValue.trim() || !sessionId || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await sendMessage(sessionId, userMessage);

      const userMsg: Message = {
        id: Date.now(),
        session_id: 0,
        role: "user",
        content: userMessage,
        sentiment: response.sentiment,
        frustration_score: response.frustration_score,
        sources: null,
        timestamp: new Date().toISOString(),
      };

      const assistantMsg: Message = {
        id: Date.now() + 1,
        session_id: 0,
        role: "assistant",
        content: response.reply,
        sentiment: response.sentiment,
        frustration_score: response.frustration_score,
        sources: response.sources,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, userMsg, assistantMsg]);
      setCurrentSentiment(response.sentiment);
      setCurrentFrustration(response.frustration_score);
      setCurrentSources(response.sources);
    } catch (error) {
      console.error("Failed to send message:", error);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  }, [inputValue, sessionId, isLoading]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (!isInitialized) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b px-6 py-4">
          <div className="flex items-center gap-3">
            <Link href="/" className="flex items-center gap-2">
              <div className="bg-primary rounded-lg p-2">
                <Bot className="h-5 w-5 text-white" />
              </div>
              <span className="font-bold text-lg text-gray-900">CustomerChat</span>
            </Link>
            <span className="flex items-center gap-1.5 text-xs text-green-600">
              <Circle className="h-2 w-2 fill-current" />
              Online
            </span>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-3xl mx-auto space-y-6">
            {messages.length === 0 && (
              <div className="text-center py-12">
                <div className="bg-primary/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Bot className="h-8 w-8 text-primary" />
                </div>
                <h2 className="text-xl font-semibold text-gray-900 mb-2">
                  Welcome to CustomerChat
                </h2>
                <p className="text-gray-600 max-w-md mx-auto">
                  Describe your IT problem below (VPN, password, access, hardware, software...) 
                  and I&apos;ll help you find a solution.
                </p>
              </div>
            )}
            {messages.map((message, index) => (
              <ChatBubble key={`${message.id}-${index}`} message={message} />
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="flex gap-3">
                  <div className="bg-secondary w-8 h-8 rounded-full flex items-center justify-center">
                    <Bot className="h-4 w-4 text-primary" />
                  </div>
                  <div className="bg-secondary rounded-2xl rounded-bl-md px-4 py-3">
                    <div className="flex gap-1">
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        <div className="bg-white border-t p-4">
          <div className="max-w-3xl mx-auto">
            <div className="flex gap-3">
              <textarea
                ref={inputRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Describe your IT problem (VPN, password, access...)"
                className="flex-1 resize-none rounded-lg border border-input bg-background px-4 py-3 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                rows={2}
                disabled={isLoading}
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputValue.trim() || isLoading}
                className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <Send className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <aside className="w-80 bg-white border-l p-4 space-y-4 overflow-y-auto hidden lg:block">
        <SentimentPanel
          sentiment={currentSentiment}
          frustrationScore={currentFrustration}
        />
        <SourcesPanel sources={currentSources} />
      </aside>
    </div>
  );
}
