import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InputChat } from './input-chat';

describe('InputChat', () => {
  let component: InputChat;
  let fixture: ComponentFixture<InputChat>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InputChat],
    }).compileComponents();

    fixture = TestBed.createComponent(InputChat);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
