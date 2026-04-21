import { TestBed } from '@angular/core/testing';

import { InputChatService } from './input-chat-service';

describe('InputChatService', () => {
  let service: InputChatService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(InputChatService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
