import { AfterViewInit, Component, ElementRef, inject } from '@angular/core';

@Component({
  selector: 'app-carousel',
  imports: [],
  templateUrl: './carousel.html',
  styleUrl: './carousel.scss',
})
export class Carousel implements AfterViewInit {
  private el = inject(ElementRef);

  ngAfterViewInit() {
    setTimeout(() => {
      
      const items = this.el.nativeElement.querySelectorAll('.carousel-item');

      if (items.length === 0) return;

      items.forEach((element: any) => {
          const minPerSlide = 3; 
          let nextElement = element.nextElementSibling;
          
          for (let i = 1; i < minPerSlide; i++) {
              if (!nextElement) {
                  nextElement = items[0];
              }
              
              const cloneChild = nextElement.cloneNode(true) as HTMLElement;
              // Garante que estamos pegando a primeira div filha (.card)
              if (cloneChild.children.length > 0) {
                  element.appendChild(cloneChild.children[0]);
              }
              nextElement = nextElement.nextElementSibling;
          }
      });

    }, 0); 
  }

}
