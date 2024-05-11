import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {BehaviorSubject, map, Observable} from "rxjs";
import {VacdataModel} from "../models/vacData.model";
import {UserModel} from "../models/user.model";
import {response} from "express";
import {Router} from "@angular/router";

@Injectable({
  providedIn: 'root'
})
export class VaccineService {

    private vacUpdateDataSubject: BehaviorSubject<any> = new BehaviorSubject<any>(null);
    public vacUpdateData$: Observable<any> = this.vacUpdateDataSubject.asObservable();
    vacData: any;

    constructor(private http: HttpClient,
                private router: Router) { }

    logout(): Observable<any> {
        return this.http.post('http://localhost:8000/api/logout', {}, { withCredentials: true });
    }
    getUserData(): Observable<any> {
        return this.http.get("http://localhost:8000/api/user", { withCredentials: true });
    }

    getUserVaccineData(): Observable<any>{
        return this.http.get("http://localhost:8000/api/userVac", { withCredentials: true });
    }

    searchVacInfoWithoutLogin(formData: any) {
        this.http.post('http://localhost:8000/api/vacInfoWithoutLogin', formData).subscribe(
            response => {
                this.vacData=response
                this.router.navigate(['/vacInfoWithoutLogin']);
            },
            (error) => {
                console.error('Search failed:', error);
            }
        );
    }

    getVacInfoWithoutLogin():any{
        return this.vacData;
    }

    getVacUpdateInfo(formData: any): Observable<any> {
        return this.http.post('http://localhost:8000/api/vacUpdatePage', formData, { withCredentials: true });
    }

    loadVacUpdateData(formData: any): void {
        this.getVacUpdateInfo(formData).subscribe(
            response => {
                this.vacUpdateDataSubject.next(response);
                this.router.navigate(['/vacUpdate']);
            },
            error => {
                console.error('Error retrieving data:', error);
            }
        );
    }
    getVacUpdateData():Observable<any>{
        return this.vacUpdateData$;
    }

    updateVaccine(data: any) {
        this.http.post('http://localhost:8000/api/vacUpdate', data, {withCredentials:true}).subscribe(
            () => {
                this.router.navigate(['/vacUpdatePage']);
            },
            (error) => {
                console.error('Vaccine Update failed:', error);
            }
        );
    }





}
