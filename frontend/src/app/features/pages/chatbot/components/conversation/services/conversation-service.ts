import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ConversationService {
  private textUser : string[] = [];

  set(text : string){
    this.textUser.push(text);
  }

  read() : string[] {
    return this.textUser
  }
}
