import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SalvePosts } from './save-posts';

describe('SalvePosts', () => {
  let component: SalvePosts;
  let fixture: ComponentFixture<SalvePosts>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SalvePosts],
    }).compileComponents();

    fixture = TestBed.createComponent(SalvePosts);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
