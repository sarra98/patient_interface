import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AppointmentService, Medecin, CreateAppointmentRequest } from '../../services/appointment.service';

@Component({
  selector: 'app-book-appointment',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './book-appointment.component.html',
  styleUrls: ['./book-appointment.component.css']
})
export class BookAppointmentComponent implements OnInit {
  medecins: Medecin[] = [];
  appointmentData: CreateAppointmentRequest = {
    medecin_id: 0,
    date_rdv: '',
    motif: '',
    notes: ''
  };
  
  isLoading = false;
  isLoadingMedecins = true;
  errorMessage = '';
  successMessage = '';
  
  // Common appointment types
  appointmentTypes = [
    'Consultation générale',
    'Consultation de suivi',
    'Consultation d\'urgence',
    'Visite de contrôle',
    'Consultation spécialisée',
    'Consultation préopératoire',
    'Consultation postopératoire',
    'Examen médical',
    'Renouvellement d\'ordonnance'
  ];

  constructor(
    private appointmentService: AppointmentService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadMedecins();
    this.setMinDate();
  }

  loadMedecins() {
    this.appointmentService.getMedecins().subscribe({
      next: (response) => {
        this.medecins = response.medecins;
        // Auto-select the first (and likely only) doctor
        if (this.medecins.length > 0) {
          this.appointmentData.medecin_id = this.medecins[0].id;
        }
        this.isLoadingMedecins = false;
      },
      error: (error) => {
        this.errorMessage = 'Erreur lors du chargement des médecins';
        this.isLoadingMedecins = false;
        console.error('Error loading medecins:', error);
      }
    });
  }

  setMinDate() {
    // Set minimum date to tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const minDate = tomorrow.toISOString().slice(0, 16);
    const dateInput = document.getElementById('date_rdv') as HTMLInputElement;
    if (dateInput) {
      dateInput.min = minDate;
    }
  }

  onMotifSelect(motif: string) {
    this.appointmentData.motif = motif;
  }

  onSubmit() {
    if (!this.isFormValid()) {
      this.errorMessage = 'Veuillez remplir tous les champs obligatoires';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.appointmentService.createAppointment(this.appointmentData).subscribe({
      next: (response) => {
        this.isLoading = false;
        this.successMessage = 'Rendez-vous créé avec succès !';
        
        // Reset form
        this.appointmentData = {
          medecin_id: this.medecins.length > 0 ? this.medecins[0].id : 0,
          date_rdv: '',
          motif: '',
          notes: ''
        };
        
        // Redirect to appointments page after a delay
        setTimeout(() => {
          this.router.navigate(['/appointments']);
        }, 2000);
      },
      error: (error) => {
        this.isLoading = false;
        this.errorMessage = error.error?.error || 'Erreur lors de la création du rendez-vous';
        
        // Scroll to top to show error
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
  }

  isFormValid(): boolean {
    return !!(
      this.appointmentData.medecin_id &&
      this.appointmentData.date_rdv &&
      this.appointmentData.motif.trim()
    );
  }

  formatDateTime(dateTime: string): string {
    if (!dateTime) return '';
    const date = new Date(dateTime);
    return date.toLocaleDateString('fr-FR', {
      weekday: 'long',
      day: '2-digit',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  getSelectedMedecin(): Medecin | undefined {
    return this.medecins.find(m => m.id === this.appointmentData.medecin_id);
  }

  isTimeSlotValid(): boolean {
    if (!this.appointmentData.date_rdv) return true;
    
    const selectedDate = new Date(this.appointmentData.date_rdv);
    const hour = selectedDate.getHours();
    const day = selectedDate.getDay(); // 0 = Sunday, 6 = Saturday
    
    // Check if it's during business hours (8h-18h) and weekdays
    if (day === 0) return false; // Sunday
    if (day === 6 && hour >= 12) return false; // Saturday after 12h
    if (hour < 8 || hour >= 18) return false; // Outside business hours
    
    return true;
  }

  getTimeSlotError(): string {
    if (!this.appointmentData.date_rdv) return '';
    
    const selectedDate = new Date(this.appointmentData.date_rdv);
    const hour = selectedDate.getHours();
    const day = selectedDate.getDay();
    
    if (day === 0) return 'Les rendez-vous ne sont pas disponibles le dimanche';
    if (day === 6 && hour >= 12) return 'Les rendez-vous du samedi ne sont disponibles que le matin (9h-12h)';
    if (hour < 8 || hour >= 18) return 'Les rendez-vous sont disponibles de 8h à 18h en semaine';
    
    return '';
  }
}
