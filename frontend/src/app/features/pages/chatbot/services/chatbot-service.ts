import { Injectable } from '@angular/core';
import { IChatConfig } from '../interfaces/chat-config';

@Injectable({
  providedIn: 'root',
})
export class ChatbotService {
  private chat : IChatConfig = {
    agent : '',
    describe : '',
    wayImg : ''
  };

  update(chat : IChatConfig | undefined) {
    if(chat) {
      this.chat = chat;
    } else {
      this.chat = {
        agent : '',
        describe : '',
        wayImg : ''
      };
    }
  }

  read() : IChatConfig {
    return this.chat;
  }
}
