export type ToolCallRecord = {
  id: string;
  tool: string;
  summary: string;
  isDone: boolean;
  resultText?: string;
  isError?: boolean;
  agentId?: string;
  agentLabel: string;
};

export type AgentMessageRecord = {
  id: string;
  turnId?: string;
  kind: "text" | "thinking" | "user";
  text: string;
  agentId?: string;
  agentLabel: string;
};

export type ToolHistoryTab = "calls" | "messages";

declare module "claude-code" {
  interface PluginState {
    "tool-history": {
      calls: ToolCallRecord[];
      messages: AgentMessageRecord[];
      isOpen: boolean;
      activeTab: ToolHistoryTab;
      fullResults: Record<string, string>;
    };
  }
}
