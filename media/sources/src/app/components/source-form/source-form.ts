import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { SourceService } from '../../services/source-service';

@Component({
  selector: 'app-source-form',
  imports: [ReactiveFormsModule],
  templateUrl: './source-form.html',
  styleUrl: './source-form.css',
})
export class SourceForm implements OnInit {
  form!: FormGroup;
  isEdit = false;
  sourceId!: number;
  loading = false;

  constructor(
    private fb: FormBuilder,
    private sourceService: SourceService,
    private route: ActivatedRoute,
    private router: Router,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.form = this.fb.group({
      name: ['', Validators.required],
      url: ['', Validators.required],
      company_id: [null, Validators.required],
      tagged_company_ids: [[]]
    });

    const idParam = this.route.snapshot.paramMap.get('id');

    if (idParam) {
      this.isEdit = true;
      this.sourceId = Number(idParam);
      this.loadSource();
    }
  }

  loadSource(): void {
    this.loading = true;

    this.sourceService.getSource(this.sourceId).subscribe({
      next: (data) => {
        this.form.patchValue({
          name: data.name,
          url: data.url,
          company_id: data.company?.id || null,
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

    const request = this.isEdit
      ? this.sourceService.updateSource(this.sourceId, this.form.value)
      : this.sourceService.createSource(this.form.value);

    request.subscribe({
      next: () => {
        this.router.navigate(['/sources/new']);
      },
      error: (err) => {
  console.error('FULL ERROR:', err);
  console.error('BACKEND ERROR:', err.error); // errors from backend
  this.loading = false;
  this.cdr.markForCheck()
}
    });
  }

  goBack(): void {
  this.router.navigate(['/sources/new']);
  }
}
