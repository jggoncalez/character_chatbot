import { Component, inject, signal, WritableSignal } from '@angular/core';
import { IChatConfig } from './interfaces/chat-config';
import { Conversation } from './components/conversation/conversation';
import { FieldTree, form, FormField } from '@angular/forms/signals';
import { IFormChatConfig } from './interfaces/form-chat-config';
import { ConversationService } from './components/conversation/services/conversation-service';
import { SideBar } from './components/side-bar/side-bar';
import { ChatbotService } from './services/chatbot-service';


@Component({
  selector: 'app-chatbot',
  imports: [Conversation, FormField,SideBar],
  templateUrl: './chatbot.html',
  styleUrl: './chatbot.scss',
})
export class Chatbot {
  conversationService = inject(ConversationService);
  chatbotService = inject(ChatbotService);
  formModel : WritableSignal<IFormChatConfig> = signal<IFormChatConfig>({
    prompt : ''
  });
  fieldForm :FieldTree<IFormChatConfig> = form(this.formModel);

  chatConfig : WritableSignal<IChatConfig> = signal<IChatConfig>(this.chatbotService.read())

  onClick() {
    // TO-DO: Melhorar a forma que o input é enviado, além de adicionar retrições caso o joão deseja
    this.conversationService.set(this.fieldForm.prompt().value())
  }
}
