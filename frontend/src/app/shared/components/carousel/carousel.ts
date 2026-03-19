import { AfterViewInit, Component, ElementRef, inject, input } from '@angular/core';
import { Card } from '../card/card';
import { IChatConfig } from '../../../features/pages/chatbot/interfaces/chat-config';

@Component({
  selector: 'app-carousel',
  imports: [Card],
  templateUrl: './carousel.html',
  styleUrl: './carousel.scss',
})
export class Carousel {
  cards = input<IChatConfig[]>([]);

  getCardAt(index: number): IChatConfig {
    const allCards = this.cards();
    if (allCards.length === 0) return {} as IChatConfig;
    
    return allCards[index % allCards.length];
  }
}
