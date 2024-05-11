import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl} from "@angular/forms";
import {HttpClient} from "@angular/common/http";
import {Router} from "@angular/router";
import {VaccineService} from "../services/vaccine.service";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit{
    loginForm: any;
    form:any;
    constructor(private formBuilder:FormBuilder,
                private http:HttpClient,
                private router: Router,
                private vaccineService: VaccineService
    ) {
    }
    ngOnInit(): void {
        this.loginForm = this.formBuilder.group({
            phone: new FormControl(''),
            password: new FormControl('')
        })

        this.form = this.formBuilder.group({
            userId: new FormControl(''),
        })
    }

    login(){
        this.http.post('http://localhost:8000/api/login', this.loginForm.getRawValue(), {withCredentials:true})
            .subscribe((response: any) => {
                const userType = response.userType;
                if (userType === 'vaccinRecipient') {
                    this.router.navigate(['/user']);
                } else {
                    this.router.navigate(['/vaccinator']);
                }
            }, (error) => {
                console.error('Login failed:', error);
            });
    }

    search() {
        const formData = this.form.getRawValue();
        this.vaccineService.searchVacInfoWithoutLogin(formData);
    }

}
