import { computed, Injectable, signal } from '@angular/core';
import { IPostConfig } from '../../../interfaces/post-config';

@Injectable({
  providedIn: 'root',
})
export class PostService {
  private readonly STORAGE_KEY = 'saved_posts';
 
  private _savedPosts = signal<IPostConfig[]>(this.loadFromStorage());
 
  getAll = computed(() => this._savedPosts());
 
  isSaved = (postId: string): boolean =>
    this._savedPosts().some((p) => p.id === postId);
 
  save(post: IPostConfig): void {
    if (this.isSaved(post.id)) return;
    const updated = [...this._savedPosts(), post];
    this._savedPosts.set(updated);
    this.setStorage(updated);
  }
 
  remove(postId: string): void {
    const updated = this._savedPosts().filter((p) => p.id !== postId);
    this._savedPosts.set(updated);
    this.setStorage(updated);
  }
 
  toggle(post: IPostConfig): void {
    if (this.isSaved(post.id)) {
      this.remove(post.id);
    } else {
      this.save(post);
    }
  }
 
  private loadFromStorage(): IPostConfig[] {
    try {
      const raw = localStorage.getItem(this.STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  }
 
  private setStorage(data: IPostConfig[]): void {
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(data));
  }
}
