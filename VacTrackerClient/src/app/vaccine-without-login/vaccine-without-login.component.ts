import { Component } from '@angular/core';
import {VaccineDetailsModel} from "../models/userVaccineDetails.model";
import {VaccineService} from "../services/vaccine.service";
import {FormBuilder, FormControl} from "@angular/forms";
import {VacdataModel} from "../models/vacData.model";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-vaccine-without-login',
  templateUrl: './vaccine-without-login.component.html',
  styleUrl: './vaccine-without-login.component.css'
})
export class VaccineWithoutLoginComponent {

    vacData:any;
    constructor(private vaccineService: VaccineService,
                private route:ActivatedRoute) {
    }
    ngOnInit(): void {
        this.vacData=this.vaccineService.getVacInfoWithoutLogin()
        console.log(this.vacData)
    }
}
