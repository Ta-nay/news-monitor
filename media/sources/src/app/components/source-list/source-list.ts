import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Observable, map, startWith } from 'rxjs';
import { Source } from '../../models/source.model';
import { SourceService } from '../../services/source-service';

@Component({
  selector: 'app-source-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './source-list.html',
  styleUrl: './source-list.css',
})
export class SourceList implements OnInit {

  sources$!: Observable<Source[]>;
  loading = true;

  constructor(
    private sourceService: SourceService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadSources();
  }

  loadSources(): void {
    this.sources$ = this.sourceService.getSources().pipe(
      map((res: any) => res.results ? res.results : res),
      startWith([]) // ensures template has initial value
    );

    this.loading = false;
  }

  createSource(): void {
    this.router.navigate(['/sources/new/create']);
  }

  editSource(id: number): void {
    this.router.navigate(['/sources/new/edit', id]);
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