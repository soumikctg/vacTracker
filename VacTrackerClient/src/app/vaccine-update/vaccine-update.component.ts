import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup} from "@angular/forms";
import {VaccineService} from "../services/vaccine.service";
import { Router} from "@angular/router";
import {Observable} from "rxjs";

@Component({
  selector: 'app-vaccine-update',
  templateUrl: './vaccine-update.component.html',
  styleUrl: './vaccine-update.component.css'
})
export class VaccineUpdateComponent implements OnInit{
    vacUpdate$: any;
    form:any;
    isReady=false;
    constructor(private formBuilder:FormBuilder,
                private vaccineService:VaccineService,
                private router:Router) {
    }
    ngOnInit(): void {
        this.vaccineService.getVacUpdateData().subscribe((data: any) => {
            this.vacUpdate$ = data;
            this.initializeForm(this.vacUpdate$);
        });

    }

    private initializeForm(vacUpdate: any): void {
        this.form = this.formBuilder.group({
            BCG1 :  new FormControl(vacUpdate?.boolean_list[0]),
            BCG2: new FormControl(vacUpdate?.boolean_list[1]),
            PENTA1: new FormControl(vacUpdate?.boolean_list[2]),
            PENTA2: new FormControl(vacUpdate?.boolean_list[3]),
            PENTA3: new FormControl(vacUpdate?.boolean_list[4]),
            OPV1: new FormControl(vacUpdate?.boolean_list[5]),
            OPV2: new FormControl(vacUpdate?.boolean_list[6]),
            OPV3: new FormControl(vacUpdate?.boolean_list[7]),
            PCV1: new FormControl(vacUpdate?.boolean_list[7]),
            PCV2: new FormControl(vacUpdate?.boolean_list[9]),
            PCV3: new FormControl(vacUpdate?.boolean_list[10]),
            IPV1: new FormControl(vacUpdate?.boolean_list[11]),
            IPV2: new FormControl(vacUpdate?.boolean_list[12]),
            MR1: new FormControl(vacUpdate?.boolean_list[13]),
            MR2: new FormControl(vacUpdate?.boolean_list[14]),
        });
        this.isReady=true;
    }

    submit(){
        var checkboxes = this.getSelectedCheckboxes();
        var data = {
            userId:this.vacUpdate$?.userId,
            checkboxes:checkboxes,
        }
        this.vaccineService.updateVaccine(data)
    }

    getSelectedCheckboxes() {
        const selectedCheckboxes: string[] = [];
        Object.keys(this.form.controls).forEach(controlName => {
            const control = this.form.controls[controlName];
            if (control.value === true) {
                selectedCheckboxes.push(controlName);
            }
        });
        return selectedCheckboxes;
    }
    logout(): void {
        this.vaccineService.logout().subscribe(
            () => {
                // Logout successful, navigate to the home page or any other page
                this.router.navigate(['/']);
            },
            (error) => {
                // Handle logout error
                console.error('Logout error:', error);
            }
        );
    }



}
