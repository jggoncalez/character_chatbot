import { Injectable, signal, WritableSignal } from '@angular/core';
import { IChatConfig } from '../interfaces/chat-config';
import { IMessage } from '../components/side-bar/interfaces/message-config';



@Injectable({
  providedIn: 'root',
})
export class ChatbotService {
  private messages = signal<IMessage[]>([]);
  private _chatConfig = signal<IChatConfig>({ agent: '', describe: '', wayImg: '' });
  
  public chatConfig = this._chatConfig.asReadonly();

  setConfig(config: IChatConfig) {
    this._chatConfig.set(config);
  }
  getConfig() {
    return this.chatConfig();
  }
  sendMessage(text: string) {

    const userMessage: IMessage = { sender: 'user', content: text };

    this.messages.update(currentMessages => [...currentMessages, userMessage]);

    
    setTimeout(() => {
      const botResponse: IMessage = { sender: 'agent', content: 'Recebi sua mensagem: ' + text };
      
      this.messages.update(updatedMessages => [...updatedMessages, botResponse]);
    }, 1000);
  }

  clearChat() {
    this.messages.set([]); 
  }
}
