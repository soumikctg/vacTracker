import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup} from "@angular/forms";
import {HttpClient} from "@angular/common/http";
import {Router} from "@angular/router";


@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrl: './registration.component.css'
})
export class RegistrationComponent implements OnInit{

    registerForm : any;
    constructor(private formBuilder:FormBuilder,
                private http:HttpClient,
                private router: Router
    ) {

    }
    ngOnInit(): void {
        this.registerForm = this.formBuilder.group({
            name: new FormControl(''),
            phone: new FormControl(''),
            userType: new FormControl(''),
            password: new FormControl('')
        });
    }

    register(){
        console.log(this.registerForm.getRawValue())
        this.http.post('http://127.0.0.1:8000/api/register', this.registerForm.getRawValue())
            .subscribe(() => this.router.navigate(['/']));
    }

}
