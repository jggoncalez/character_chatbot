import { Component, inject, signal } from '@angular/core';
import { ThemeService } from '../../../shared/services/theme-service';
import { FeedService } from './service/feed-service';
import { IFeedModel } from './interface/feed-model';
import { form, minLength, required, FormField } from '@angular/forms/signals';
import { Post } from '../../../shared/components/post/post';

@Component({
  selector: 'app-feed',
  imports: [FormField, Post],
  templateUrl: './feed.html',
  styleUrl: './feed.scss',
})
export class Feed {
  themeService = inject(ThemeService);
  feedService = inject(FeedService);

  posts         = this.feedService.posts;
  loading       = this.feedService.loading;

  inputFeed = signal<IFeedModel>({
    inputUser : ''
  });

  formFeed = form(this.inputFeed,(schema) => {
    required(schema.inputUser,{message : "Precisa inserir alguma informacao!"})
    minLength(schema.inputUser,10,{message : "Precisa ter no minimo 10 letras!"})
  })

  onSubmitPost() {
    this.feedService.sumbitFeed(this.inputFeed())
    this.inputFeed.set({
      inputUser : ''
    })
  }

  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }

}
