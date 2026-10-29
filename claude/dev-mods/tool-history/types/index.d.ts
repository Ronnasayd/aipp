export type ToolCallRecord = {
  id: string;
  tool: string;
  summary: string;
  isDone: boolean;
  resultText?: string;
  isError?: boolean;
  agentId?: string;
  agentLabel: string;
  at?: number;
};

export type AgentMessageRecord = {
  id: string;
  turnId?: string;
  kind: "text" | "thinking" | "user" | "agent";
  text: string;
  agentId?: string;
  agentLabel: string;
  at?: number;
};

export type ToolHistoryTab = "calls" | "messages" | "all";

declare module "claude-code" {
  interface PluginState {
    "tool-history": {
      calls: ToolCallRecord[];
      messages: AgentMessageRecord[];
      isOpen: boolean;
      isCollapsed: boolean;
      isAtBottom: boolean;
      activeTab: ToolHistoryTab;
      fullResults: Record<string, string>;
    };
  }
}
