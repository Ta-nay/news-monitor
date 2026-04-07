import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { SourceService } from '../../services/source-service';
import { CommonModule } from '@angular/common';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatChipsModule } from '@angular/material/chips';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { debounceTime, distinctUntilChanged, Observable, of, startWith, switchMap } from 'rxjs';
import { CompanyService } from '../../services/company-service';
import { Company } from '../../models/source.model';

@Component({
  selector: 'app-source-form',
  imports: [
  CommonModule,
  ReactiveFormsModule,
  MatAutocompleteModule,
  MatChipsModule,
  MatInputModule,
  MatIconModule
],
  templateUrl: './source-form.html',
  styleUrl: './source-form.css',
})
export class SourceForm implements OnInit {
  form!: FormGroup;
  isEdit = false;
  sourceId!: number;
  loading = false;
  companies$!: Observable<Company[]>;
  selectedCompanies: Company[] = [];
  searchControl!: FormControl;
  
  constructor(
    private fb: FormBuilder,
    private companyService: CompanyService,
    private route: ActivatedRoute,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private sourceService: SourceService,
  ) {}

  
  

  ngOnInit(): void {
    this.searchControl = this.fb.control('');
    this.form = this.fb.group({
      name: ['', Validators.required],
      url: ['', Validators.required],
      tagged_company_ids: [[]]
    });

    const idParam = this.route.snapshot.paramMap.get('id');

    if (idParam) {
      this.isEdit = true;
      this.sourceId = Number(idParam);
      this.loadSource();
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

  addCompany(company: Company) {
    const exists = this.selectedCompanies.some(c => c.id === company.id);
    if (exists) return;
    this.selectedCompanies.push(company);
    this.form.patchValue({
      tagged_company_ids: this.selectedCompanies.map(c => c.id)
    });
    this.searchControl.setValue('');
  }

  removeCompany(company: Company) {
    this.selectedCompanies = this.selectedCompanies.filter(c => c.id !== company.id);
    this.form.patchValue({
      tagged_company_ids: this.selectedCompanies.map(c => c.id)
    });
  }

  displayFn(company: Company): string {
    return company?.name || '';
  }

  loadSource(): void {
    this.loading = true;

    this.sourceService.getSource(this.sourceId).subscribe({
      next: (data) => {
        this.selectedCompanies = data.tagged_companies || [];
        this.form.patchValue({
          name: data.name,
          url: data.url,
          tagged_company_ids: data.tagged_companies
            ? data.tagged_companies.map((c: any) => c.id)
            : []
        });
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error('Failed to load source', err);
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }

  submit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    // console.log('PAYLOAD:', this.form.value);
    const request = this.isEdit
      ? this.sourceService.updateSource(this.sourceId, this.form.value)
      : this.sourceService.createSource(this.form.value);
    request.subscribe({
      next: () => {
        this.router.navigate(['/sources/new']);
      },
      error: (err) => {
        console.error('FULL ERROR:', err);
        console.error('BACKEND ERROR:', err.error); 
        this.loading = false;
        this.cdr.markForCheck()
      }
    });
  }

  goBack(): void {
  this.router.navigate(['/sources/new']);
  }
}
