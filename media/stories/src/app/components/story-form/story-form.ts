import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { StoryService } from '../../services/story-service';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatChipsModule } from '@angular/material/chips';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { debounceTime, distinctUntilChanged, Observable, of, startWith, switchMap } from 'rxjs';
import { CompanyService } from '../../services/company-service';
import { Company } from '../../models/story.models';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Inject } from '@angular/core';

@Component({
  selector: 'app-story-form',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatAutocompleteModule,
    MatChipsModule,
    MatInputModule,
    MatIconModule,
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
    private dialogRef: MatDialogRef<StoryForm>,
    @Inject(MAT_DIALOG_DATA) public data: any,
  ) {}

  ngOnInit(): void {
    this.searchControl = this.fb.control('');
    this.form = this.fb.group({
      title: ['', Validators.required],
      body_text: [''],
      url: [
    '',
    [
      Validators.required,
      Validators.pattern(/^(https?:\/\/)?([\w\-]+\.)+[\w\-]+(\/[\w\-._~:/?#[\]@!$&'()*+,;=]*)?$/),
    ],
  ],
      tagged_company_ids: [[]],
    });

    if (this.data?.story) {
      const story = this.data.story;

      this.selectedCompanies = story.tagged_companies || [];

      this.form.patchValue({
        title: story.title,
        body_text: story.body_text,
        url: story.url,
        tagged_company_ids: this.selectedCompanies.map((c: Company) => c.id),
      });
    }

    this.companies$ = this.searchControl.valueChanges.pipe(
      startWith(''),
      debounceTime(300),
      distinctUntilChanged(),
      switchMap((term) =>
        typeof term === 'string' ? this.companyService.searchCompanies(term) : of([]),
      ),
    );
  }

  addCompany(company: Company) {
    const exists = this.selectedCompanies.some((c) => c.id === company.id);
    if (exists) return;

    this.selectedCompanies.push(company);

    this.form.patchValue({
      tagged_company_ids: this.selectedCompanies.map((c) => c.id),
    });

    this.searchControl.setValue('');
  }

  removeCompany(company: Company) {
    this.selectedCompanies = this.selectedCompanies.filter((c) => c.id !== company.id);

    this.form.patchValue({
      tagged_company_ids: this.selectedCompanies.map((c) => c.id),
    });
  }

  displayFn(company: Company): string {
    return company?.name || '';
  }

  // loadStory(): void {
  //   this.storyService.getStory(this.storyId).subscribe((data) => {
  //     // console.log('Story ID:', this.route.snapshot.paramMap.get('id'));
  //     this.form.patchValue({
  //       title: data.title,
  //       body_text: data.body_text,
  //       url: data.url,
  //       // company_id: data.company?.id,
  //       // source_id: data.source?.id,
  //       tagged_company_ids: data.tagged_companies
  //         ? data.tagged_companies.map((c: Company) => c.id)
  //         : [],
  //     });
  //     this.loading = false;
  //     this.cdr.markForCheck();
  //   });
  // }

  submit() {
    if (this.form.invalid) return;
    const raw = this.form.value;
    this.loading = true;
    // console.log('PAYLOAD:', this.form.value);

    const request = this.data?.story
      ? this.storyService.updateStory(this.data.story.id, raw)
      : this.storyService.createStory(raw);

    request.subscribe({
      next: (res) => {
        this.dialogRef.close(res); // return data to parent
      },
      error: (err) => {
        console.error(err);
      },
    });
  }
  close(): void {
    this.dialogRef.close();
  }

  goBack() {
    this.router.navigate(['/stories/new']);
  }
}
