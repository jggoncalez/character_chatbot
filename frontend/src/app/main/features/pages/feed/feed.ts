import { Component, inject, signal } from '@angular/core';
import { ThemeService } from '../../../shared/services/theme-service';
import { DatePipe, NgClass } from '@angular/common';
import { ApiService } from '../../../shared/services/api-service';
import { IPostConfig } from '../../../shared/interfaces/post-config';
import { ToastService } from '../../../shared/components/toast-messages/services/toast-service';

@Component({
  selector: 'app-feed',
  imports: [DatePipe],
  templateUrl: './feed.html',
  styleUrl: './feed.scss',
})
export class Feed {
  themeService = inject(ThemeService);
  apiService = inject(ApiService);
  toastService = inject(ToastService);

  posts = signal<IPostConfig[]>([]);
  loading = signal(false);
  posting = signal(false);
  commentInputs = signal<Record<string, string>>({});
  openComments = signal<Record<string, boolean>>({});

  constructor() {
    this.loadFeed();
  }

  loadFeed() {
    this.loading.set(true);
    this.apiService.getFeed().subscribe({
      next: (data) => { this.posts.set(data); this.loading.set(false); },
      error: () => this.loading.set(false)
    });
  }

  toggleComments(postId: string) {
    this.openComments.update(state => ({ ...state, [postId]: !state[postId] }));
  }

  updateInput(postId: string, value: string) {
    this.commentInputs.update(state => ({ ...state, [postId]: value }));
  }

  submitComment(postId: string) {
    const text = this.commentInputs()[postId];
    if(text.length > 200) {
      this.toastService.show('Mensagem muito grande',"danger",2000);
      return
    }
    if (!text?.trim()) return;
    this.posting.set(true);
    this.apiService.postFeed(postId, text).subscribe({
      next: (value : any) => {
        this.toastService.show(`${value.message}`,"success",1500);
        this.updateInput(postId, '');
        this.posting.set(false);
        this.loadFeed();
      },
      error: () => this.posting.set(false)
    });
  }

  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }
}
