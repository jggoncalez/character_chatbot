import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Modal } from './shared/components/modal/modal';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,Modal],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('frontend');
}
