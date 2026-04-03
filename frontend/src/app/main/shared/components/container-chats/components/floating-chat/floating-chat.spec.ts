import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FloatingChat } from './floating-chat';

describe('FloatingChat', () => {
  let component: FloatingChat;
  let fixture: ComponentFixture<FloatingChat>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FloatingChat],
    }).compileComponents();

    fixture = TestBed.createComponent(FloatingChat);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
