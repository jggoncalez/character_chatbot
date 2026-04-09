import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContainerChats } from './container-chats';

describe('ContainerChats', () => {
  let component: ContainerChats;
  let fixture: ComponentFixture<ContainerChats>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ContainerChats],
    }).compileComponents();

    fixture = TestBed.createComponent(ContainerChats);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
