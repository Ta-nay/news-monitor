import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { StoryService } from '../../services/story-service';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatChipsModule } from '@angular/material/chips';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { debounceTime, distinctUntilChanged, Observable, of, startWith, switchMap } from 'rxjs';
import { CompanyService } from '../../services/company-service';


@Component({
  selector: 'app-story-form',
  imports: [
  CommonModule,
  ReactiveFormsModule,
  MatAutocompleteModule,
  MatChipsModule,
  MatInputModule,
  MatIconModule
],
  templateUrl: './story-form.html',
  styleUrl: './story-form.css',
})
export class StoryForm implements OnInit {
  form!: FormGroup;
  isEdit = false;
  storyId!: number;
  loading = false;
  companies$!: Observable<any[]>;
  selectedCompanies: any[] = [];
  searchControl!: FormControl;

  constructor(
    private fb: FormBuilder,
    private storyService: StoryService,
    private route: ActivatedRoute,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private companyService: CompanyService,
  ) {}

  ngOnInit(): void {
    this.searchControl = this.fb.control('');
    this.form = this.fb.group({
      title: ['', Validators.required],
      body_text: [''],
      url: ['', Validators.required],
      tagged_company_ids: [[]]
    });

    const id = this.route.snapshot.paramMap.get('id');

    if (id) {
      this.isEdit = true;
      this.storyId = +id;
      this.loadStory();
    }

    this.companies$ = this.searchControl.valueChanges.pipe(
      startWith(''),
      debounceTime(300),
      distinctUntilChanged(),
      switchMap(term =>
        typeof term === 'string'
          ? this.companyService.searchCompanies(term)
          : of([])
      )
    );
  }

  addCompany(company: any) {
    const exists = this.selectedCompanies.some(c => c.id === company.id);
    if (exists) return;

    this.selectedCompanies.push(company);

    this.form.patchValue({
      tagged_company_ids: this.selectedCompanies.map(c => c.id)
    });

    this.searchControl.setValue('');
  }

  removeCompany(company: any) {
    this.selectedCompanies = this.selectedCompanies.filter(c => c.id !== company.id);

    this.form.patchValue({
      tagged_company_ids: this.selectedCompanies.map(c => c.id)
    });
  }

  displayFn(company: any): string {
    return company?.name || '';
  }

  loadStory() {
    this.storyService.getStory(this.storyId).subscribe((data) => {
      // console.log('Story ID:', this.route.snapshot.paramMap.get('id'));
      this.form.patchValue({
        title: data.title,
        body_text: data.body_text,
        url: data.url,
        // company_id: data.company?.id,
        // source_id: data.source?.id,
        tagged_company_ids: data.tagged_companies
            ? data.tagged_companies.map((c: any) => c.id)
            : []
      });
      this.loading = false;
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
    tagged_companies: raw.tagged_company_ids
  };
  this.loading = true;
    console.log('PAYLOAD:', this.form.value);

  const request = this.isEdit
    ? this.storyService.updateStory(this.storyId, raw)
    : this.storyService.createStory(raw);

  request.subscribe({
    next: () => this.router.navigate(['/stories/new']),
    error: (err) => {
  console.error('FULL ERROR:', err);
  console.error('BACKEND ERROR:', err.error); 
  this.loading = false;
  this.cdr.markForCheck()
}
  });
}

  goBack() {
    this.router.navigate(['/stories/new']);
  }
}