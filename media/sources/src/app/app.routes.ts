import { Routes } from '@angular/router';
import { SourceList } from './components/source-list/source-list';
import { SourceForm } from './components/source-form/source-form';

export const routes: Routes = [
    { path : 'sources/new', component : SourceList },
    { path : 'sources/new/create', component: SourceForm},
    { path : 'sources/new/edit/:id', component: SourceForm},
];
