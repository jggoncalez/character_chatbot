export interface IMessage {
    sender : 'user' | 'agent',
    content : string,
    state? : 'happy' | 'sad' | 'angry' | 'neutral' | 'hushed'
}
