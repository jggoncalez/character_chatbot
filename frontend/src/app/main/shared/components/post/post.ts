import { Component, inject, input } from '@angular/core';
import { IPostConfig } from '../../interfaces/post-config';
import { AgentImage } from '../agent-image/agent-image';
import { DatePipe } from '@angular/common';
import { FeedService } from '../../../features/pages/feed/service/feed-service';
import { ThemeService } from '../../services/theme-service';
import { PostService } from './service/post-service';

@Component({
  selector: 'app-post',
  imports: [DatePipe,AgentImage],
  templateUrl: './post.html',
  styleUrl: './post.scss',
})
export class Post {
  saveFeedService = inject(PostService);
  themeService = inject(ThemeService);
  feedService = inject(FeedService);

  post = input.required<IPostConfig>();
  posting       = this.feedService.posting;
  commentInputs = this.feedService.commentInputs;
  openComments  = this.feedService.openComments;
  

  onKeyDown(event: KeyboardEvent,postId : string): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.feedService.submitComment(postId);
    }
  }

  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }
  
}
