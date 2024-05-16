import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RegistrationComponent } from './registration/registration.component';
import { HomeComponent } from './home/home.component';
import {RouterLink} from "@angular/router";
import {HttpClientModule, provideHttpClient, withFetch} from "@angular/common/http";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { UserPageComponent } from './user-page/user-page.component';
import { VaccinatorPageComponent } from './vaccinator-page/vaccinator-page.component';
import { VaccineWithoutLoginComponent } from './vaccine-without-login/vaccine-without-login.component';
import { VaccineUpdateComponent } from './vaccine-update/vaccine-update.component';
import {ToastrModule} from "ngx-toastr";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";

@NgModule({
  declarations: [
    AppComponent,
    RegistrationComponent,
    HomeComponent,
    UserPageComponent,
    VaccinatorPageComponent,
    VaccineWithoutLoginComponent,
    VaccineUpdateComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    RouterLink,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    ToastrModule.forRoot({
      timeOut: 10000,
      positionClass: 'toast-bottom-right',
      preventDuplicates: false,
    })
  ],
  providers: [
    provideClientHydration(),
    provideHttpClient(withFetch())
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
