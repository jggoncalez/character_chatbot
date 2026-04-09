export interface IHistoryMessages { 
    role: 'user' | 'model',
    content: string,
    state? : 'happy' | 'sad' | 'angry' | 'neutral' | 'hushed'
}