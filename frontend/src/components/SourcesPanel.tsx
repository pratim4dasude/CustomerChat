"use client";

import { SourceItem } from "@/types";
import { BookOpen, Tag } from "lucide-react";
import * as Tooltip from "@radix-ui/react-tooltip";

interface SourcesPanelProps {
  sources: SourceItem[] | null;
}

export function SourcesPanel({ sources }: SourcesPanelProps) {
  if (!sources || sources.length === 0) {
    return (
      <div className="bg-white rounded-xl p-4 shadow-md">
        <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
          <BookOpen className="h-4 w-4" />
          Sources
        </h3>
        <p className="text-sm text-muted-foreground">No sources available yet</p>
      </div>
    );
  }

  return (
    <Tooltip.Provider delayDuration={200}>
      <div className="bg-white rounded-xl p-4 shadow-md">
        <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
          <BookOpen className="h-4 w-4" />
          Sources ({sources.length})
        </h3>

        <div className="space-y-2 max-h-64 overflow-y-auto">
          {sources.map((source, index) => (
            <Tooltip.Root key={`${source.ki_id}-${index}`}>
              <Tooltip.Trigger asChild>
                <div className="p-3 bg-secondary/50 rounded-lg cursor-help hover:bg-secondary transition-colors">
                  <p className="font-medium text-sm text-gray-900 line-clamp-2">
                    {source.title}
                  </p>
                  {source.category && (
                    <span className="inline-flex items-center gap-1 mt-1 text-xs text-primary">
                      <Tag className="h-3 w-3" />
                      {source.category}
                    </span>
                  )}
                </div>
              </Tooltip.Trigger>
              <Tooltip.Portal>
                <Tooltip.Content
                  className="max-w-xs p-3 bg-gray-900 text-white text-xs rounded-lg shadow-xl z-50"
                  sideOffset={5}
                >
                  <p className="font-medium mb-2">{source.title}</p>
                  {source.snippet && (
                    <p className="text-gray-300 text-xs leading-relaxed">
                      {source.snippet}
                    </p>
                  )}
                  <Tooltip.Arrow className="fill-gray-900" />
                </Tooltip.Content>
              </Tooltip.Portal>
            </Tooltip.Root>
          ))}
        </div>
      </div>
    </Tooltip.Provider>
  );
}
