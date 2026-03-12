import { Component } from '@angular/core';
import { Carousel } from '../../../shared/components/carousel/carousel';

@Component({
  selector: 'app-home-page',
  imports: [Carousel],
  templateUrl: './home-page.html',
  styleUrl: './home-page.scss',
})
export class HomePage {}
