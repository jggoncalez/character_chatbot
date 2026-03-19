import { Component, inject } from '@angular/core';
import { ConversationService } from '../conversation/services/conversation-service';
import { DatePipe } from '@angular/common';
import { Router } from '@angular/router';



@Component({
  selector: 'app-side-bar',
  imports: [DatePipe],
  templateUrl: './side-bar.html',
  styleUrl: './side-bar.scss',
})
export class SideBar {
  conversationService = inject(ConversationService);
  router = inject(Router);
  history = this.conversationService.getHistory();

  novoChat() {
    this.conversationService.currentChat.set(null);
    this.router.navigate(['']);
  }
}
