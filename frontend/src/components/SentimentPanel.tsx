"use client";

import { Smile, Meh, Frown } from "lucide-react";

interface SentimentPanelProps {
  sentiment: string | null;
  frustrationScore: number | null;
}

export function SentimentPanel({ sentiment, frustrationScore }: SentimentPanelProps) {
  if (!sentiment) {
    return (
      <div className="bg-white rounded-xl p-4 shadow-md">
        <h3 className="font-semibold text-gray-900 mb-3">Sentiment Analysis</h3>
        <p className="text-sm text-muted-foreground">No analysis available yet</p>
      </div>
    );
  }

  const getSentimentIcon = () => {
    switch (sentiment) {
      case "positive":
        return <Smile className="h-5 w-5 text-green-500" />;
      case "negative":
        return <Frown className="h-5 w-5 text-red-500" />;
      default:
        return <Meh className="h-5 w-5 text-yellow-500" />;
    }
  };

  const getSentimentColor = () => {
    switch (sentiment) {
      case "positive":
        return "text-green-600 bg-green-50";
      case "negative":
        return "text-red-600 bg-red-50";
      default:
        return "text-yellow-600 bg-yellow-50";
    }
  };

  return (
    <div className="bg-white rounded-xl p-4 shadow-md">
      <h3 className="font-semibold text-gray-900 mb-3">Sentiment Analysis</h3>
      
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          {getSentimentIcon()}
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSentimentColor()}`}>
            {sentiment.charAt(0).toUpperCase() + sentiment.slice(1)}
          </span>
        </div>

        {frustrationScore !== null && (
          <div>
            <p className="text-xs text-muted-foreground mb-1">Frustration Score</p>
            <div className="flex items-center gap-2">
              <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className={`h-full transition-all ${
                    frustrationScore < 0.4
                      ? "bg-green-500"
                      : frustrationScore < 0.7
                      ? "bg-yellow-500"
                      : "bg-red-500"
                  }`}
                  style={{ width: `${frustrationScore * 100}%` }}
                />
              </div>
              <span className="text-sm font-medium">{Math.round(frustrationScore * 100)}%</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
