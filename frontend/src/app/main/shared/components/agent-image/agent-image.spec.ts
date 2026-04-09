import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AgentImage } from './agent-image';

describe('AgentImage', () => {
  let component: AgentImage;
  let fixture: ComponentFixture<AgentImage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AgentImage],
    }).compileComponents();

    fixture = TestBed.createComponent(AgentImage);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
