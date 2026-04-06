import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { debounceTime, map, Observable, startWith, switchMap, tap } from 'rxjs';
import { StoryService } from '../../services/story-service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Story } from '../../models/story.models';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';

@Component({
  selector: 'app-story-list',
  imports: [CommonModule, ReactiveFormsModule,MatPaginatorModule],
  templateUrl: './story-list.html',
  styleUrl: './story-list.css',
})
export class StoryList implements OnInit {
  searchControl = new FormControl('');
  stories: Story[] = [];
  loading = true;

  // pagination state
  page = 1;
  totalItems = 0;

  constructor(
    private storyService: StoryService,
    private router: Router,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.loadStories();
  }

  onSearch() {
  this.page = 1;        // reset pagination
  this.loadStories();   // trigger API call
}

  loadStories(): void {
  this.loading = true;

  this.storyService
    .getStories(this.searchControl.value|| '', this.page)
    .subscribe((res: any) => {
      this.stories = res.results;
      this.totalItems = res.count; // important!
      this.loading = false;
      this.cdr.markForCheck();
    });
}

  onPageChange(event: PageEvent) {
  this.page = event.pageIndex + 1;
  this.loadStories();
  this.cdr.markForCheck();
}

  createStory() {
    this.router.navigate(['/stories/new/create']);
  }

  editStory(id: number) {
    this.router.navigate(['/stories/new/edit', id]);
  }

  deleteStory(id: number) {
    if (!confirm('Delete this story?')) return;

    this.storyService.deleteStory(id).subscribe(() => {
      this.loadStories();
    });
  }
}

