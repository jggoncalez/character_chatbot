import { Component, computed, inject, signal, WritableSignal } from '@angular/core';
import { Conversation } from './components/conversation/conversation';
import { FieldTree, form, FormField, min, minLength, required, } from '@angular/forms/signals';
import { IFormChatConfig } from './interfaces/form-chat-config';
import { ConversationService } from './components/conversation/services/conversation-service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-chatbot',
  imports: [Conversation, FormField],
  templateUrl: './chatbot.html',
  styleUrl: './chatbot.scss',
})
export class Chatbot {
  router = inject(Router);

  conversationService = inject(ConversationService);
  formModel : WritableSignal<IFormChatConfig> = signal<IFormChatConfig>({
    prompt : ''
  });
  fieldForm: FieldTree<IFormChatConfig> = form(this.formModel, (path) => {
      required(path.prompt)
      minLength(path.prompt, 3)
    }
  );

  chatConfig = computed(() => this.conversationService.currentChat()?.config);
  
  isExpanded = false;
  onClick() {
    if (this.fieldForm.prompt().invalid()) return;

    const textoDigitado = this.fieldForm.prompt().value().trim();
    this.conversationService.set(textoDigitado);

    this.formModel.update(valores => ({ ...valores, prompt: '' }));
  }

  get isDisabled(): boolean {
    return this.fieldForm.prompt().invalid();
  }

  voltar() {
    this.conversationService.currentChat.set(null);
    this.router.navigate(['']);
  }

  

  toggleExpand() {
    if (window.innerWidth <= 768) {
      this.isExpanded = !this.isExpanded;
    }
}
}

