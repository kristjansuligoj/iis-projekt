import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GenerateMusicFormComponent } from './generate-music-form.component';

describe('GenerateMusicFormComponent', () => {
  let component: GenerateMusicFormComponent;
  let fixture: ComponentFixture<GenerateMusicFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GenerateMusicFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(GenerateMusicFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
