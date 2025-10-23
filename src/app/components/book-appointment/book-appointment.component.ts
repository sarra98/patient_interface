import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-book-appointment',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './book-appointment.component.html',
  styleUrls: ['./book-appointment.component.css']
})
export class BookAppointmentComponent implements OnInit {
  medecins: any[] = [];
  appointmentData: any = {
    medecin_id: '',
    date_rdv: '',
    motif: '',
    notes: ''
  };
  successMessage = '';
  errorMessage = '';
  isLoading = false;
  minDate = '';

  constructor(private http: HttpClient, private router: Router) {
    // Date minimale = demain
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    this.minDate = tomorrow.toISOString().split('T')[0];
  }



  ngOnInit(): void {
    this.loadMedecins();
  }

  loadMedecins(): void {
    // Utiliser l'endpoint correct avec authentification
    const token = localStorage.getItem('token');
    const headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };

    this.http.get<any>('http://localhost:5000/api/appointments/medecins', { headers }).subscribe({
      next: (response) => {
        this.medecins = response.medecins || [];
        console.log('Médecins chargés:', this.medecins);
      },
      error: (err) => {
        console.error('Erreur chargement médecins:', err);
        this.errorMessage = 'Erreur lors du chargement des médecins';
      }
    });
  }


  onSubmit(): void {
    this.isLoading = true;
    this.http.post<any>('http://localhost:5000/api/appointments', this.appointmentData).subscribe({
      next: (_res) => {
        this.successMessage = 'Rendez-vous créé avec succès';
        setTimeout(() => this.router.navigate(['/appointments']), 2000);
        this.isLoading = false;
      },
      error: (_err) => {
        this.errorMessage = "Erreur lors de la création du rendez-vous.";
        this.isLoading = false;
      }
    });
  }
  
}
