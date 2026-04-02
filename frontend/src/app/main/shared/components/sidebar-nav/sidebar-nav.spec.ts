import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SidebarNav } from './sidebar-nav';

describe('SidebarNav', () => {
  let component: SidebarNav;
  let fixture: ComponentFixture<SidebarNav>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SidebarNav],
    }).compileComponents();

    fixture = TestBed.createComponent(SidebarNav);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
