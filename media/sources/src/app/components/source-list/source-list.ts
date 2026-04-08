import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Observable, map, startWith } from 'rxjs';
import { Source } from '../../models/source.model';
import { PaginatedResponse, SourceService } from '../../services/source-service';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatDialog } from '@angular/material/dialog';
import { SourceForm } from '../source-form/source-form';

@Component({
  selector: 'app-source-list',
  standalone: true,
  imports: [CommonModule,ReactiveFormsModule,MatPaginatorModule],
  templateUrl: './source-list.html',
  styleUrl: './source-list.css',
})
export class SourceList implements OnInit {

  searchControl : FormControl = new FormControl('');
  sources : Source[] = [];
  loading : boolean= true;

  // pagination state
  page : number = 1;
  totalItems : number = 0;

  constructor(
    private sourceService: SourceService,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private dialog: MatDialog,
  ) {}

  ngOnInit(): void {
    this.loadSources();
    
  }

  onSearch():void{
    this.page = 1;
    this.loadSources();
  }

  loadSources(): void {
    this.loading = true;

    this.sourceService
      .getSources(this.searchControl.value || '', this.page)
      .subscribe((res: PaginatedResponse<Source>) => {
        this.sources = res.results;
        this.totalItems = res.count;
        this.loading = false;
        this.cdr.markForCheck();
      });
  }

  onPageChange(event: PageEvent) {
    this.page = event.pageIndex + 1;
    this.loadSources();
    this.cdr.markForCheck();
  }

  // createSource(): void {
  //   this.router.navigate(['/sources/new/create']);
  // }

  // editSource(id: number): void {
  //   this.router.navigate(['/sources/new/edit', id]);
  // }

  openCreate() {
  const dialogRef = this.dialog.open(SourceForm, {
    width: '600px'
  });

  dialogRef.afterClosed().subscribe(result => {
    if (result) {
      this.loadSources();
    }
  });
  }

  openEdit(source: Source) {
  const dialogRef = this.dialog.open(SourceForm, {
    width: '600px',
    data: { source } 
  });

  dialogRef.afterClosed().subscribe(result => {
    if (result) {
      this.loadSources();
    }
  });
}
    
  deleteSource(id: number): void {
    if (!confirm('Delete this source?')) return;
    this.sourceService.deleteSource(id).subscribe({
      next: () => {
        this.loadSources(); // refresh stream
      },
      error: (err) => {
        console.error('Delete failed', err);
      }
    });
  }
}