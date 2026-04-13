import { Component, inject, signal } from '@angular/core';
import { ThemeService } from '../../../shared/services/theme-service';
import { DatePipe } from '@angular/common';
import { FeedService } from './service/feed-service';
import { AgentImage } from '../../../shared/components/agent-image/agent-image';
import { IFeedModel } from './interface/feed-model';
import { form, minLength, required, FormField } from '@angular/forms/signals';

@Component({
  selector: 'app-feed',
  imports: [DatePipe, AgentImage, FormField],
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

  inputFeed = signal<IFeedModel>({
    inputUser : ''
  });

  formFeed = form(this.inputFeed,(schema) => {
    required(schema.inputUser,{message : "Precisa inserir alguma informacao!"})
    minLength(schema.inputUser,10,{message : "Precisa ter no minimo 10 letras!"})
  })

  onKeyDown(event: KeyboardEvent,postId : string): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.feedService.submitComment(postId);
    }
  }

  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }

  onSubmitPost() {
    this.feedService.sumbitFeed(this.inputFeed())
    this.inputFeed.set({
      inputUser : ''
    })
  }
}
