import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {HomeComponent} from "./home/home.component";
import {RegistrationComponent} from "./registration/registration.component";
import {UserPageComponent} from "./user-page/user-page.component";
import {VaccinatorPageComponent} from "./vaccinator-page/vaccinator-page.component";
import {VaccineWithoutLoginComponent} from "./vaccine-without-login/vaccine-without-login.component";
import {VaccineUpdateComponent} from "./vaccine-update/vaccine-update.component";

const routes: Routes = [
    {path: '', component: HomeComponent},
    {path: 'registration', component: RegistrationComponent},
    {path: 'user', component: UserPageComponent},
    {path: 'vaccinator', component: VaccinatorPageComponent},
    {path: 'vacInfoWithoutLogin', component: VaccineWithoutLoginComponent},
    {path: 'vacUpdate', component: VaccineUpdateComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
