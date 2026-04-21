import { computed, inject, Injectable, signal } from '@angular/core';
import { ToastService } from '../../../../shared/components/toast-messages/services/toast-service';
import { ApiService } from '../../../../shared/services/api-service';
import { IPostConfig } from '../../../../shared/interfaces/post-config';
import { IFeedModel } from '../interface/feed-model';

@Injectable({
  providedIn: 'root',
})
export class FeedService {
  private apiService = inject(ApiService);
  private toastService = inject(ToastService);

  _posts = signal<IPostConfig[]>([]);
  _loading = signal(false);
  _posting = signal(false);
  _commentInputs = signal<Record<string, string>>({});
  _openComments = signal<Record<string, boolean>>({});
  
  posts = computed(() => this._posts());
  loading = computed(() => this._loading());
  posting = computed(() => this._posting());
  commentInputs = computed(() => this._commentInputs());
  openComments = computed(() => this._openComments());

  constructor() {
    this.loadFeed();

    setTimeout(() => {
      this.loadFeedIa();
      this.loadFeed();
    }, 300000);
  }

  loadFeed(): void {
    this._loading.set(true);
    this.apiService.getFeed().subscribe({
      next: (data) => { this._posts.set(data); this._loading.set(false); },
      error: () => this._loading.set(false)
    });
  }

  loadFeedIa(): void {
    this._loading.set(true);
    this.apiService.geratingFeed().subscribe({
      next: (data) => { this._posts.set(data); this._loading.set(false); },
      error: () => this._loading.set(false)
    });
  }

  toggleComments(postId: string): void {
    this._openComments.update(state => ({ ...state, [postId]: !state[postId] }));
  }

  updateInput(postId: string, value: string): void {
    this._commentInputs.update(state => ({ ...state, [postId]: value }));
  }

  submitComment(postId: string): void {
    const text = this._commentInputs()[postId];
    if (text.length > 200) {
      this.toastService.show('Mensagem muito grande', 'danger', 2000);
      return;
    }
    if (!text?.trim()) return;

    this._posting.set(true);
    this.apiService.postCommentFeed(postId, text).subscribe({
      next: (value: any) => {
        this.toastService.show(`${value.message}`, 'success', 1500);
        this.updateInput(postId, '');
        this._posting.set(false);
        this.loadFeed();
      },
      error: () => this._posting.set(false)
    });
  }

  sumbitFeed(model : IFeedModel) {
    const text = model.inputUser;

    this._posting.set(true);

    this.apiService.postFeedUser(text).subscribe(
      {
        next: (value : IPostConfig) => {
          this.toastService.show(`Feed Atualizado!!`,`success`,3000);
          this._posting.set(false);
          this.loadFeed();
        },
        error : () => this._posting.set(false)
      }
    )
  }
}
