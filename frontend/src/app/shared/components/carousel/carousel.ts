import { AfterViewInit, Component, ElementRef, inject, input } from '@angular/core';
import { Card } from '../card/card';
import { IChatConfig } from '../../../features/pages/chatbot/interfaces/chat-config';

@Component({
  selector: 'app-carousel',
  imports: [Card],
  templateUrl: './carousel.html',
  styleUrl: './carousel.scss',
})
export class Carousel implements AfterViewInit {
  private element = inject(ElementRef);
  cards = input<IChatConfig[]>([]);

  ngAfterViewInit() {
    setTimeout(() => {
      
      const items = this.element.nativeElement.querySelectorAll('.carousel-item');

      if (items.length === 0) return;

      items.forEach((element: any) => {
          const minCard = 3; 
          let nextElement = element.nextElementSibling;
          
          for (let i = 1; i < minCard; i++) {
              if (!nextElement) {
                  nextElement = items[0];
              }
              
              const cloneChild = nextElement.cloneNode(true) as HTMLElement;
              if (cloneChild.children.length > 0) {
                  element.appendChild(cloneChild.children[0]);
              }
              nextElement = nextElement.nextElementSibling;
          }
      });

    }, 0); 
  }

}
