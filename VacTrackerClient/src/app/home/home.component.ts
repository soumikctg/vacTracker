import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl} from "@angular/forms";
import {HttpClient} from "@angular/common/http";
import {Router} from "@angular/router";
import {VaccineService} from "../services/vaccine.service";
import {ToastrService} from "ngx-toastr";

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
                private vaccineService: VaccineService,
                private toastrService: ToastrService
    ) {
    }
    ngOnInit(): void {
        this.loginForm = this.formBuilder.group({
            userId: new FormControl(''),
            password: new FormControl('')
        })

        this.form = this.formBuilder.group({
            userId: new FormControl(''),
        })
    }

    login(){
        this.http.post('http://localhost:8000/api/login', this.loginForm.getRawValue(), {withCredentials:true})
            .subscribe((response: any) => {
                console.log(response);
                const userType = response.userType;
                if (userType === 'vaccineRecipient') {
                    this.router.navigate(['/user']);
                } else {
                    this.router.navigate(['/vaccinator']);
                }
            }, (error) => {
                this.toastrService.error(error.error.detail, 'Login failed');
                console.error('Login failed:', error.error.detail);
            });
    }

    search() {
        const formData = this.form.getRawValue()
        this.vaccineService.searchVacInfoWithoutLogin(formData)
    }

}
