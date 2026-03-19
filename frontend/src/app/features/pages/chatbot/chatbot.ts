import { Component, computed, inject, signal, WritableSignal } from '@angular/core';
import { Conversation } from './components/conversation/conversation';
import { FieldTree, form, FormField, min, minLength, required, } from '@angular/forms/signals';
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
  fieldForm: FieldTree<IFormChatConfig> = form(this.formModel, (path) => {
      required(path.prompt)
      minLength(path.prompt, 3)
    }
  );

  chatConfig = computed(() => this.chatbotService.chatConfig());

  onClick() {

    if (this.fieldForm.prompt().invalid()) return;

    const textoDigitado = this.fieldForm.prompt().value().trim();
    this.conversationService.set(textoDigitado);

    this.formModel.update(valores => ({ ...valores, prompt: '' }));
  }

  get isDisabled(): boolean {
    return this.fieldForm.prompt().invalid();
  }
}

