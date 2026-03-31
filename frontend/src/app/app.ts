import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ToastMessages } from './shared/components/toast-messages/toast-messages';
import { Header } from './shared/components/header/header';
import { SidebarNav } from './shared/components/sidebar-nav/sidebar-nav';
import { SidebarRemember } from './shared/components/sidebar-remember/sidebar-remember';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,ToastMessages,Header,SidebarNav,SidebarRemember],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('frontend');
}
