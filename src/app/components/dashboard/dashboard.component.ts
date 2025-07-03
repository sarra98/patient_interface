import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService, Patient } from '../../services/auth.service';
import { AppointmentService, Appointment } from '../../services/appointment.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  currentPatient: Patient | null = null;
  appointments: Appointment[] = [];
  upcomingAppointments: Appointment[] = [];
  isLoading = true;
  error = '';

  constructor(
    private authService: AuthService,
    private appointmentService: AppointmentService
  ) {}

  ngOnInit() {
    this.currentPatient = this.authService.getCurrentPatient();
    this.loadAppointments();
  }

  loadAppointments() {
    this.appointmentService.getAppointments().subscribe({
      next: (response) => {
        this.appointments = response.appointments;
        this.upcomingAppointments = this.appointments
          .filter(apt => {
            const aptDate = new Date(apt.date_rdv);
            const now = new Date();
            return aptDate > now && apt.statut !== 'annule';
          })
          .slice(0, 3); // Show only next 3 appointments
        this.isLoading = false;
      },
      error: (error) => {
        this.error = 'Erreur lors du chargement des rendez-vous';
        this.isLoading = false;
        console.error('Error loading appointments:', error);
      }
    });
  }

  get totalAppointments(): number {
    return this.appointments.length;
  }

  get confirmedAppointments(): number {
    return this.appointments.filter(apt => apt.statut === 'confirme').length;
  }

  get pendingAppointments(): number {
    return this.appointments.filter(apt => apt.statut === 'planifie').length;
  }

  get completedAppointments(): number {
    return this.appointments.filter(apt => apt.statut === 'termine').length;
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  }

  formatTime(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  getStatusLabel(status: string): string {
    return this.appointmentService.getStatusLabel(status);
  }

  getStatusClass(status: string): string {
    return this.appointmentService.getStatusClass(status);
  }
}
