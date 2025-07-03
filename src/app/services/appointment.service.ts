import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

export interface Medecin {
  id: number;
  nom: string;
  prenom: string;
  nom_complet: string;
  specialite: string;
  telephone?: string;
  email?: string;
  horaires?: string;
  is_active: boolean;
}

export interface Appointment {
  id: number;
  patient_id: number;
  medecin_id: number;
  date_rdv: string;
  duree: number;
  motif: string;
  statut: 'planifie' | 'confirme' | 'annule' | 'termine';
  notes?: string;
  created_at: string;
  medecin?: Medecin;
  patient?: {
    id: number;
    nom: string;
    prenom: string;
  };
}

export interface CreateAppointmentRequest {
  medecin_id: number;
  date_rdv: string;
  motif: string;
  notes?: string;
}

export interface UpdateAppointmentRequest {
  statut?: 'planifie' | 'confirme' | 'annule' | 'termine';
  notes?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AppointmentService {
  private apiUrl = '/api/appointments';

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {}

  private getHeaders() {
    return { headers: this.authService.getAuthHeaders() };
  }

  getMedecins(): Observable<{ medecins: Medecin[] }> {
    return this.http.get<{ medecins: Medecin[] }>(`${this.apiUrl}/medecins`, this.getHeaders());
  }

  getAppointments(): Observable<{ appointments: Appointment[] }> {
    return this.http.get<{ appointments: Appointment[] }>(`${this.apiUrl}/`, this.getHeaders());
  }

  createAppointment(appointmentData: CreateAppointmentRequest): Observable<{ message: string; appointment: Appointment }> {
    return this.http.post<{ message: string; appointment: Appointment }>(
      `${this.apiUrl}/`,
      appointmentData,
      this.getHeaders()
    );
  }

  updateAppointment(appointmentId: number, updateData: UpdateAppointmentRequest): Observable<{ message: string; appointment: Appointment }> {
    return this.http.put<{ message: string; appointment: Appointment }>(
      `${this.apiUrl}/${appointmentId}`,
      updateData,
      this.getHeaders()
    );
  }

  cancelAppointment(appointmentId: number): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(
      `${this.apiUrl}/${appointmentId}`,
      this.getHeaders()
    );
  }

  getStatusLabel(status: string): string {
    switch (status) {
      case 'planifie': return 'Planifié';
      case 'confirme': return 'Confirmé';
      case 'annule': return 'Annulé';
      case 'termine': return 'Terminé';
      default: return status;
    }
  }

  getStatusClass(status: string): string {
    switch (status) {
      case 'planifie': return 'bg-info';
      case 'confirme': return 'bg-success';
      case 'annule': return 'bg-danger';
      case 'termine': return 'bg-warning';
      default: return 'bg-secondary';
    }
  }
}
