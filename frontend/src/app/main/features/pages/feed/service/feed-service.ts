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
 
  private _posts = signal<IPostConfig[]>([]);
  private _loading = signal(false);
  private _posting = signal(false);
  private _commentInputs = signal<Record<string, string>>({});
  private _openComments = signal<Record<string, boolean>>({});
  
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
      error: (error) => {
        this._loading.set(false);
        const status = error?.status;
        if (status === 500) {
          this.toastService.show('Erro ao carregar o feed. Tente novamente mais tarde.', 'danger', 4000);
        } else if (status === 0) {
          this.toastService.show('Sem conexão com o servidor. Verifique sua rede.', 'danger', 4000);
        } else {
          this.toastService.show('Não foi possível carregar o feed.', 'danger', 3000);
        }
      }
    });
  }
 
  loadFeedIa(): void {
    this._loading.set(true);
    this.apiService.geratingFeed().subscribe({
      next: (data) => { this._posts.set(data); this._loading.set(false); },
      error: (error) => {
        this._loading.set(false);
        const status = error?.status;
        if (status === 500) {
          this.toastService.show('Erro ao gerar novos posts. O serviço de IA está indisponível.', 'danger', 4000);
        } else if (status === 0) {
          this.toastService.show('Sem conexão com o servidor ao tentar gerar posts.', 'danger', 4000);
        } else {
          this.toastService.show('Não foi possível gerar novos posts.', 'danger', 3000);
        }
      }
    });
  }
 
  toggleComments(postId: string): void {
    this._openComments.update(state => ({ ...state, [postId]: !state[postId] }));
  }
 
  updateInput(postId: string, value: string): void {
    this._commentInputs.update(state => ({ ...state, [postId]: value }));
  }
 
  submitComment(postId: string): void {
    const text = this._commentInputs()[postId] ?? '';
    if (text.length > 200) {
      this.toastService.show('Mensagem muito grande', 'danger', 2000);
      return;
    }
    if (!text.trim()) return;
 
    this._posting.set(true);
    this.apiService.postCommentFeed(postId, text).subscribe({
      next: (value: any) => {
        this.toastService.show(`${value.message}`, 'success', 1500);
        this.updateInput(postId, '');
        this._posting.set(false);
        this.loadFeed();
      },
      error: (error) => {
        this._posting.set(false);
        const status = error?.status;
        if (status === 404) {
          this.toastService.show('Post não encontrado. Atualize o feed e tente novamente.', 'danger', 4000);
        } else if (status === 422) {
          this.toastService.show('Comentário inválido. Verifique o texto e tente novamente.', 'danger', 3000);
        } else if (status === 500) {
          this.toastService.show('Não foi possível enviar o comentário. Tente novamente.', 'danger', 4000);
        } else if (status === 0) {
          this.toastService.show('Sem conexão com o servidor.', 'danger', 3000);
        } else {
          this.toastService.show('Erro ao enviar comentário. Tente novamente.', 'danger', 3000);
        }
      }
    });
  }
 
  sumbitFeed(model: IFeedModel) {
    const text = model.inputUser;
 
    this._posting.set(true);
 
    this.apiService.postFeedUser(text).subscribe({
      next: (value: IPostConfig) => {
        this.toastService.show('Feed Atualizado!!', 'success', 3000);
        this._posting.set(false);
        this.loadFeed();
      },
      error: (error) => {
        this._posting.set(false);
        const status = error?.status;
        if (status === 422) {
          this.toastService.show('Texto inválido. Use entre 1 e 500 caracteres.', 'danger', 3000);
        } else if (status === 500) {
          this.toastService.show('Não foi possível publicar o post. Tente novamente.', 'danger', 4000);
        } else if (status === 0) {
          this.toastService.show('Sem conexão com o servidor.', 'danger', 3000);
        } else {
          this.toastService.show('Erro ao publicar. Tente novamente.', 'danger', 3000);
        }
      }
    });
  }
}
