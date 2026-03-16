import { Component, signal, WritableSignal } from '@angular/core';
import { IChatConfig } from './interfaces/chat-config';
import { Conversation } from './components/conversation/conversation';
import { FieldTree } from '@angular/forms/signals';
import { IFormChatConfig } from './interfaces/form-chat-config';


@Component({
  selector: 'app-chatbot',
  imports: [Conversation],
  templateUrl: './chatbot.html',
  styleUrl: './chatbot.scss',
})
export class Chatbot {
  fieldForm! :FieldTree<IFormChatConfig>;

  chatConfig : WritableSignal<IChatConfig> = signal<IChatConfig>({
    name : "Steve",
    describe : "Em busca de Diamantes",
    styleTheme : 
    {
      primaryColor : "#dadaea",
      secundaryColor : "#d0d0ea",
      configColor : "#00aeaa"
    },
    wayImg : "https://placehold.co/40"
  })

  onInput() {
    throw Error('method not implement')
  }
}
