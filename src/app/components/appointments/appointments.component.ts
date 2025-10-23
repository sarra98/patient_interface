import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { AppointmentService, Appointment } from '../../services/appointment.service';

@Component({
  selector: 'app-appointments',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './appointments.component.html',
  styleUrls: ['./appointments.component.css']
})
export class AppointmentsComponent implements OnInit {
  appointments: Appointment[] = [];
  filteredAppointments: Appointment[] = [];
  isLoading = true;
  error = '';
  successMessage = '';
  currentFilter = 'all';

  showEditModal = false;
  editAppointmentData: any = null;

  constructor(
    private appointmentService: AppointmentService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadAppointments();
  }

  loadAppointments() {
    this.isLoading = true;
    this.appointmentService.getAppointments().subscribe({
      next: (response) => {
        this.appointments = response.appointments.sort((a, b) => 
          new Date(b.date_rdv).getTime() - new Date(a.date_rdv).getTime()
        );
        this.applyFilter(this.currentFilter);
        this.isLoading = false;
      },
      error: (error) => {
        this.error = 'Erreur lors du chargement des rendez-vous';
        this.isLoading = false;
        console.error('Error loading appointments:', error);
      }
    });
  }

  applyFilter(filter: string) {
    this.currentFilter = filter;
    switch (filter) {
      case 'upcoming':
        this.filteredAppointments = this.appointments.filter(apt => {
          const aptDate = new Date(apt.date_rdv);
          const now = new Date();
          return aptDate > now && apt.statut !== 'annule';
        });
        break;
      case 'past':
        this.filteredAppointments = this.appointments.filter(apt => {
          const aptDate = new Date(apt.date_rdv);
          const now = new Date();
          return aptDate <= now || apt.statut === 'termine';
        });
        break;
      case 'cancelled':
        this.filteredAppointments = this.appointments.filter(apt => apt.statut === 'annule');
        break;
      default:
        this.filteredAppointments = [...this.appointments];
    }
  }

  editAppointment(appointment: Appointment) {
    // Ouvre le modal et clone les données pour édition
    this.editAppointmentData = { ...appointment };
    // Pour datetime-local, il faut un format 'YYYY-MM-DDTHH:mm'
    this.editAppointmentData.date_rdv = this.editAppointmentData.date_rdv?.slice(0, 16);
    this.showEditModal = true;
  }

  closeEditModal() {
    this.showEditModal = false;
    this.editAppointmentData = null;
  }

  saveEditAppointment() {
    if (!this.editAppointmentData) return;

    // Préparer les données avec la date au bon format
    const updateData = { ...this.editAppointmentData };
    if (updateData.date_rdv) {
      // Convertir la date locale en ISO pour le serveur
      const localDate = new Date(updateData.date_rdv);
      updateData.date_rdv = localDate.toISOString();
    }

    this.appointmentService.updateAppointment(this.editAppointmentData.id, updateData).subscribe({
      next: (_response) => {
        this.successMessage = 'Rendez-vous modifié avec succès';
        this.closeEditModal();
        this.loadAppointments();
        setTimeout(() => this.successMessage = '', 5000);
      },
      error: (error) => {
        this.error = error.error?.error || 'Erreur lors de la modification';
        setTimeout(() => this.error = '', 5000);
      }
    });
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      weekday: 'long',
      day: '2-digit',
      month: 'long',
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

  canCancelAppointment(appointment: Appointment): boolean {
    const aptDate = new Date(appointment.date_rdv);
    const now = new Date();
    const hoursDiff = (aptDate.getTime() - now.getTime()) / (1000 * 3600);

    return hoursDiff > 24 &&
           appointment.statut !== 'annule' &&
           appointment.statut !== 'termine';
  }

  canEditAppointment(appointment: Appointment): boolean {
    const aptDate = new Date(appointment.date_rdv);
    const now = new Date();
    const hoursDiff = (aptDate.getTime() - now.getTime()) / (1000 * 3600);

    return hoursDiff > 24 &&
           appointment.statut !== 'annule' &&
           appointment.statut !== 'termine';
  }

  cancelAppointment(appointment: Appointment) {
    if (!confirm('Êtes-vous sûr de vouloir annuler ce rendez-vous ?')) {
      return;
    }

    this.appointmentService.cancelAppointment(appointment.id).subscribe({
      next: (_response) => {
        this.successMessage = 'Rendez-vous annulé avec succès';
        this.loadAppointments();
        setTimeout(() => this.successMessage = '', 5000);
      },
      error: (error) => {
        this.error = error.error?.error || 'Erreur lors de l\'annulation';
        setTimeout(() => this.error = '', 5000);
      }
    });
  }

  payAppointment(appointment: Appointment) {
    // Rediriger vers la page de paiement avec l'ID du rendez-vous
    this.router.navigate(['/payment', appointment.id]);
  }

  isPastAppointment(appointment: Appointment): boolean {
    const aptDate = new Date(appointment.date_rdv);
    const now = new Date();
    return aptDate <= now;
  }

  getFilterButtonClass(filter: string): string {
    return this.currentFilter === filter ? 'btn-primary' : 'btn-outline-primary';
  }

  get appointmentCounts() {
    const now = new Date();
    return {
      all: this.appointments.length,
      upcoming: this.appointments.filter(apt => {
        const aptDate = new Date(apt.date_rdv);
        return aptDate > now && apt.statut !== 'annule';
      }).length,
      past: this.appointments.filter(apt => {
        const aptDate = new Date(apt.date_rdv);
        return aptDate <= now || apt.statut === 'termine';
      }).length,
      cancelled: this.appointments.filter(apt => apt.statut === 'annule').length
    };
  }
}
