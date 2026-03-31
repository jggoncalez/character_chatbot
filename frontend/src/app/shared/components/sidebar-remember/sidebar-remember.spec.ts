import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SidebarRemember } from './sidebar-remember';

describe('SidebarRemember', () => {
  let component: SidebarRemember;
  let fixture: ComponentFixture<SidebarRemember>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SidebarRemember],
    }).compileComponents();

    fixture = TestBed.createComponent(SidebarRemember);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
