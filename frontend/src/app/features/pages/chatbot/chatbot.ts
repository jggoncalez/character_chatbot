import { Component, inject, signal, WritableSignal } from '@angular/core';
import { IChatConfig } from './interfaces/chat-config';
import { Conversation } from './components/conversation/conversation';
import { FieldTree, form, FormField } from '@angular/forms/signals';
import { IFormChatConfig } from './interfaces/form-chat-config';
import { ConversationService } from './components/conversation/services/conversation-service';


@Component({
  selector: 'app-chatbot',
  imports: [Conversation, FormField],
  templateUrl: './chatbot.html',
  styleUrl: './chatbot.scss',
})
export class Chatbot {
  conversationService = inject(ConversationService);
  formModel : WritableSignal<IFormChatConfig> = signal<IFormChatConfig>({
    prompt : ''
  });
  fieldForm :FieldTree<IFormChatConfig> = form(this.formModel);

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

  onClick() {
    // TO-DO: Melhorar a forma que o input é enviado, além de adicionar retrições caso o joão deseja
    this.conversationService.set(this.fieldForm.prompt().value())
  }
}
