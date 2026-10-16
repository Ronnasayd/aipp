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

declare module "claude-code" {
  interface PluginState {
    "tool-history": { calls: ToolCallRecord[]; isOpen: boolean };
  }
}
