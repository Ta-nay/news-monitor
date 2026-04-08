import { Routes } from '@angular/router';
import { StoryList } from './components/story-list/story-list';
import { StoryForm } from './components/story-form/story-form';

export const routes: Routes = [
  { path: 'stories/new', component: StoryList },
  { path: 'stories/new/create', component: StoryForm },
  { path: 'stories/new/edit/:id', component: StoryForm },
];
