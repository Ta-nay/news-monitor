import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { StoryService } from '../../services/story-service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-story-form',
  imports: [ReactiveFormsModule],
  templateUrl: './story-form.html',
  styleUrl: './story-form.css',
})
export class StoryForm implements OnInit {
  form!: FormGroup;
  isEdit = false;
  storyId!: number;

  constructor(
    private fb: FormBuilder,
    private storyService: StoryService,
    private route: ActivatedRoute,
    private router: Router,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {

    this.form = this.fb.group({
      title: ['', Validators.required],
      body_text: [''],
      url: ['', Validators.required],
      company_id: [null, Validators.required],
      source_id: [null, Validators.required],
      tagged_company_ids: [[]]
    });

    const id = this.route.snapshot.paramMap.get('id');

    if (id) {
      this.isEdit = true;
      this.storyId = +id;
      this.loadStory();
    }
  }

  loadStory() {
    this.storyService.getStory(this.storyId).subscribe((data) => {
      console.log('Story ID:', this.route.snapshot.paramMap.get('id'));
      this.form.patchValue({
        title: data.title,
        body_text: data.body_text,
        url: data.url,
        company_id: data.company?.id,
        source_id: data.source?.id,
        tagged_company_ids: data.tagged_companies.map((c: any) => c.id)
      });
      this.cdr.markForCheck();
    });
  }
  
  submit() {
  if (this.form.invalid) return;

  const raw = this.form.value;

  const payload = {
    title: raw.title,
    body_text: raw.body_text,
    url: raw.url,
    company: raw.company_id,
    source: raw.source_id,
    tagged_companies: raw.tagged_company_ids
  };

  const request = this.isEdit
    ? this.storyService.updateStory(this.storyId, payload)
    : this.storyService.createStory(payload);

  request.subscribe({
    next: () => this.router.navigate(['/stories']),
    error: (err) => {
      console.error(err.error);
      alert(JSON.stringify(err.error));
    }
  });
}

  goBack() {
    this.router.navigate(['/stories/new']);
  }
}