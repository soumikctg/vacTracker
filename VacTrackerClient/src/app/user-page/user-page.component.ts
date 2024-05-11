import { Component } from '@angular/core';
import {VaccineService} from "../services/vaccine.service";
import {UserModel} from "../models/user.model";
import {HttpClient} from "@angular/common/http";
import {response} from "express";
import {Router} from "@angular/router";
import {VacdataModel} from "../models/vacData.model";

@Component({
  selector: 'app-user-page',
  templateUrl: './user-page.component.html',
  styleUrl: './user-page.component.css'
})
export class UserPageComponent {

    vacData:any;
    user:any;
    constructor(private vaccineService: VaccineService,
                private http:HttpClient,
                private router: Router
    ) {
    }
    ngOnInit(): void {
        const userId = 2;

        this.userData();


        this.vaccineService.getUserVaccineData().subscribe(
            (data: VacdataModel) => {
                this.vacData = data;
                console.log(this.vacData);
            },
            error => {
                console.error('Error fetching user data:', error);
            }
        );


        // this.vaccineService.getUserInfo().subscribe(
        //     (data : UserModel) => {
        //         this.user=data;
        //         console.log(this.user)
        //     },
        //     error => console.error('Error fetching user info')
        // )

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
