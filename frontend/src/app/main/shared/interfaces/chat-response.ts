export interface IChatResponse {
  character: string;
  text: string;
  state: 'happy' | 'sad' | 'angry' | 'neutral' | 'hushed';
}
