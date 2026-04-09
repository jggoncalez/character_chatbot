import { TestBed } from '@angular/core/testing';

import { ContainerChatService } from './container-chat-service';

describe('ContainerChatService', () => {
  let service: ContainerChatService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ContainerChatService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
