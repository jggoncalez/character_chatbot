import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ToastMessages } from './main/shared/components/toast-messages/toast-messages';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,ToastMessages],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('frontend');
}
