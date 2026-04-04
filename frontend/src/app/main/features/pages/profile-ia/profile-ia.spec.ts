import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileIA } from './profile-ia';

describe('ProfileIA', () => {
  let component: ProfileIA;
  let fixture: ComponentFixture<ProfileIA>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProfileIA],
    }).compileComponents();

    fixture = TestBed.createComponent(ProfileIA);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
