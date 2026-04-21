import { Component, inject } from '@angular/core';
import { IPostConfig } from '../../../shared/interfaces/post-config';
import { ThemeService } from '../../../shared/services/theme-service';
import { PostService } from '../../../shared/components/post/service/post-service';
import { Post } from '../../../shared/components/post/post';

@Component({
  selector: 'app-save-posts',
  imports: [Post],
  templateUrl: './save-posts.html',
  styleUrl: './save-posts.scss',
})
export class SalvePosts {
  themeService = inject(ThemeService);
  postService = inject(PostService);

  getSavePosts() : IPostConfig[] {
    return this.postService.getAll()
  }

  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }
}
