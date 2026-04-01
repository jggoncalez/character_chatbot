import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Modal } from './shared/components/modal/modal';
import { ToastMessages } from './shared/components/toast-messages/toast-messages';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,Modal,ToastMessages],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('frontend');
}
