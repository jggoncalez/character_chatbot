import { TestBed } from '@angular/core/testing';

import { SavePostsService } from './save-posts-service';

describe('SavePostsService', () => {
  let service: SavePostsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SavePostsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
