import { inject, Injectable, signal } from '@angular/core';
import { ToastService } from '../../../../shared/components/toast-messages/services/toast-service';
import { ApiService } from '../../../../shared/services/api-service';
import { IPostConfig } from '../../../../shared/interfaces/post-config';

@Injectable({
  providedIn: 'root',
})
export class FeedService {
  private apiService = inject(ApiService);
  private toastService = inject(ToastService);

  posts = signal<IPostConfig[]>([]);
  loading = signal(false);
  posting = signal(false);
  commentInputs = signal<Record<string, string>>({});
  openComments = signal<Record<string, boolean>>({});

  constructor() {
    this.loadFeedIa();
    this.loadFeed();

    setInterval(() => {
      this.loadFeedIa();
      this.loadFeed();
    }, 300000);
  }

  loadFeed(): void {
    this.loading.set(true);
    this.apiService.getFeed().subscribe({
      next: (data) => { this.posts.set(data); this.loading.set(false); },
      error: () => this.loading.set(false)
    });
  }

  loadFeedIa(): void {
    this.loading.set(true);
    this.apiService.geratingFeed().subscribe({
      next: (data) => { this.posts.set(data); this.loading.set(false); },
      error: () => this.loading.set(false)
    });
  }

  toggleComments(postId: string): void {
    this.openComments.update(state => ({ ...state, [postId]: !state[postId] }));
  }

  updateInput(postId: string, value: string): void {
    this.commentInputs.update(state => ({ ...state, [postId]: value }));
  }

  submitComment(postId: string): void {
    const text = this.commentInputs()[postId];
    if (text.length > 200) {
      this.toastService.show('Mensagem muito grande', 'danger', 2000);
      return;
    }
    if (!text?.trim()) return;

    this.posting.set(true);
    this.apiService.postFeed(postId, text).subscribe({
      next: (value: any) => {
        this.toastService.show(`${value.message}`, 'success', 1500);
        this.updateInput(postId, '');
        this.posting.set(false);
        this.loadFeed();
      },
      error: () => this.posting.set(false)
    });
  }
}
