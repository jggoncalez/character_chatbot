import { Component, inject } from '@angular/core';
import { ThemeService } from '../../../shared/services/theme-service';
import { DatePipe } from '@angular/common';
import { FeedService } from './service/feed-service';
import { AgentImage } from '../../../shared/components/agent-image/agent-image';

@Component({
  selector: 'app-feed',
  imports: [DatePipe, AgentImage],
  templateUrl: './feed.html',
  styleUrl: './feed.scss',
})
export class Feed {
  themeService = inject(ThemeService);
  feedService = inject(FeedService);

  posts         = this.feedService.posts;
  loading       = this.feedService.loading;
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
