export interface IHistoryResponse {
  character: string;
  history: { role: 'user' | 'model'; content: string }[];
}
