import { Component, OnInit } from '@angular/core';
import { debounceTime, map, Observable, startWith, switchMap, tap } from 'rxjs';
import { StoryService } from '../../services/story-service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Story } from '../../models/story.models';
import { FormControl, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-story-list',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './story-list.html',
  styleUrl: './story-list.css',
})
export class StoryList implements OnInit {
  searchControl = new FormControl('');
  stories$!: Observable<Story[]>;
  loading = true;

  constructor(
    private storyService: StoryService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadStories(); // initial load

  this.searchControl.valueChanges.pipe(
    debounceTime(300),
    switchMap(value => {
      if (!value) return this.storyService.getStories();
      return this.storyService.getStories(value);
    })
  ).subscribe((data: any) => {
    this.stories$ = data;
  });
  }

  // loadStories(): void {
  //   this.stories$ = this.storyService.getStories().pipe(
  //     map((res: any) => res.results ? res.results : res),
  //           startWith([]) // ensures template has initial value
  //         );
  //     this.loading = false;
  // }
  
loadStories(): void {
  this.stories$ = this.storyService.getStories().pipe(
    map((res: any) => res.results ? res.results : res),
    tap(() => this.loading = false), // ✅ runs when data arrives
    startWith([])
  );
  this.loading = false;
}

  createStory() {
    this.router.navigate(['/stories/new/create']);
  }

  editStory(id: number) {
    this.router.navigate(['/stories/new/edit', id]);
  }

  deleteStory(id: number) {
    if (!confirm('Delete this story?')) return;

    this.storyService.deleteStory(id).subscribe({
      next: () => this.loadStories(),
      error: (err) => console.error(err)
    });
  }
}

