import { Injectable, signal, WritableSignal } from '@angular/core';
import { IHistoryConfig } from '../../side-bar/interfaces/history-config';
import { IChatConfig } from '../../../interfaces/chat-config';

@Injectable({
  providedIn: 'root',
})
export class ConversationService {

  public currentChat: WritableSignal<IHistoryConfig> = signal<IHistoryConfig>({
    config : {
      agent : '',
      describe : '',
      wayImg : ''
    },
    messages : []
  });
  
  set(text: string, config : IChatConfig) {
    if(this.currentChat()) {
      this.currentChat.set({
        config : config,
        messages : [
          {
            sender : 'user',
            content : text
          }
        ]
      });
    } else {
      this.currentChat.update(chatState => ({
          ...chatState,
          messages : [...chatState.messages, {sender : 'user', content : text}]
        })
      )
    }
    
    // TO-DO: Integração do Back end 
    setTimeout(() => {
      this.currentChat.update(chatState => ({
        ...chatState,
        messages: [...chatState.messages, { sender: 'agent', content: 'Recebi sua mensagem: ' + text }]
      }));
    }, 1000);
  }
  
  get() {
    return this.currentChat()
  }
}
