"use client";

import Link from "next/link";
import { Bot, Zap, Shield, MessageSquare } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <div className="bg-primary rounded-lg p-2">
                <Bot className="h-6 w-6 text-white" />
              </div>
              <span className="font-bold text-xl text-gray-900">CustomerChat</span>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            <span className="text-primary">CustomerChat</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Contextual IT Support Chatbot powered by RAG, Pinecone, and ChatGPT.
            <br />
            Get instant help with your IT issues.
          </p>
          <Link
            href="/chat"
            className="inline-flex items-center gap-2 bg-primary text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-primary/90 transition-colors shadow-lg shadow-primary/25"
          >
            <MessageSquare className="h-5 w-5" />
            Start Chat
          </Link>
        </div>

        <div className="mt-24 grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<Zap className="h-8 w-8 text-primary" />}
            title="Instant Responses"
            description="Get immediate answers from our knowledge base powered by AI and vector search."
          />
          <FeatureCard
            icon={<Shield className="h-8 w-8 text-primary" />}
            title="Accurate Information"
            description="All answers are generated from verified IT support documentation."
          />
          <FeatureCard
            icon={<Bot className="h-8 w-8 text-primary" />}
            title="Smart Context"
            description="Uses conversation history and RAG to provide contextual support."
          />
        </div>

        <div className="mt-24 bg-white rounded-2xl shadow-xl p-8 md:p-12">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-6 text-center">
            How It Works
          </h2>
          <div className="grid md:grid-cols-4 gap-6">
            <Step number={1} text="Ask your IT question" />
            <Step number={2} text="We search the knowledge base" />
            <Step number={3} text="AI generates relevant answer" />
            <Step number={4} text="Get your solution instantly" />
          </div>
        </div>
      </main>

      <footer className="border-t bg-white mt-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <p className="text-center text-gray-500">
            CustomerChat - IT Support Chatbot powered by RAG, Pinecone, and ChatGPT
          </p>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}

function Step({ number, text }: { number: number; text: string }) {
  return (
    <div className="text-center">
      <div className="w-10 h-10 bg-primary text-white rounded-full flex items-center justify-center mx-auto mb-3 font-bold">
        {number}
      </div>
      <p className="text-gray-700 font-medium">{text}</p>
    </div>
  );
}
