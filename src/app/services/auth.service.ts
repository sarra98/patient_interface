import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';

export interface Patient {
  id: number;
  prenom: string;
  nom: string;
  email: string;
  telephone: string;
  date_naissance: string;
  adresse?: string;
  antecedents_medicaux?: string;
  contact_urgence_nom: string;
  contact_urgence_telephone: string;
  created_at: string;
  is_active: boolean;
}

export interface LoginResponse {
  message: string;
  patient: Patient;
  access_token: string;
  refresh_token: string;
}

export interface RegisterRequest {
  prenom: string;
  nom: string;
  email: string;
  telephone: string;
  date_naissance: string;
  adresse?: string;
  antecedents_medicaux?: string;
  contact_urgence_nom: string;
  contact_urgence_telephone: string;
  password: string;
  confirm_password: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = '/api/auth';
  private currentPatientSubject = new BehaviorSubject<Patient | null>(null);
  public currentPatient$ = this.currentPatientSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadStoredAuth();
  }

  private loadStoredAuth() {
    const token = localStorage.getItem('access_token');
    const patient = localStorage.getItem('current_patient');
    
    if (token && patient) {
      try {
        const patientData = JSON.parse(patient);
        this.currentPatientSubject.next(patientData);
      } catch (error) {
        console.error('Error parsing stored patient data:', error);
        this.logout();
      }
    }
  }

  login(email: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/login`, { email, password })
      .pipe(
        tap(response => {
          localStorage.setItem('access_token', response.access_token);
          localStorage.setItem('refresh_token', response.refresh_token);
          localStorage.setItem('current_patient', JSON.stringify(response.patient));
          this.currentPatientSubject.next(response.patient);
        })
      );
  }

  register(registerData: RegisterRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/register`, registerData)
      .pipe(
        tap(response => {
          localStorage.setItem('access_token', response.access_token);
          localStorage.setItem('refresh_token', response.refresh_token);
          localStorage.setItem('current_patient', JSON.stringify(response.patient));
          this.currentPatientSubject.next(response.patient);
        })
      );
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('current_patient');
    this.currentPatientSubject.next(null);
  }

  isAuthenticated(): boolean {
    return localStorage.getItem('access_token') !== null;
  }

  getCurrentPatient(): Patient | null {
    return this.currentPatientSubject.value;
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  getAuthHeaders(): HttpHeaders {
    const token = this.getToken();
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
  }

  refreshToken(): Observable<any> {
    const refreshToken = localStorage.getItem('refresh_token');
    return this.http.post(`${this.apiUrl}/refresh`, {}, {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${refreshToken}`
      })
    }).pipe(
      tap((response: any) => {
        localStorage.setItem('access_token', response.access_token);
      })
    );
  }
}
