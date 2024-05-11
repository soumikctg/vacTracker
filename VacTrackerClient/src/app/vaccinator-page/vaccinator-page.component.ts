import {Component, OnInit} from '@angular/core';
import {VacdataModel} from "../models/vacData.model";
import {VaccineService} from "../services/vaccine.service";
import {HttpClient} from "@angular/common/http";
import {Router} from "@angular/router";
import {UserModel} from "../models/user.model";
import {FormBuilder, FormControl} from "@angular/forms";

@Component({
  selector: 'app-vaccinator-page',
  templateUrl: './vaccinator-page.component.html',
  styleUrl: './vaccinator-page.component.css'
})
export class VaccinatorPageComponent implements OnInit{

    user:UserModel|undefined;
    form:any;
    constructor(private vaccineService: VaccineService,
                private router: Router,
                private formBuilder:FormBuilder
    ) {
    }
    ngOnInit(): void {
        this.form = this.formBuilder.group({
            userId: new FormControl(''),
        })
        this.userData();
    }

    userData(){
        this.vaccineService.getUserData().subscribe(
            (response: any) => {
                this.user = response;
            },
            (error: any) => {
                console.error('Error fetching user data:', error);
            }
        );
    }

    search() {
        const formData = this.form.getRawValue();
        this.vaccineService.loadVacUpdateData(formData);
    }


}
