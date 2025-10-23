import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { PaymentService, PaymentRequest } from '../../services/payment.service';
import { AppointmentService, Appointment } from '../../services/appointment.service';

@Component({
  selector: 'app-payment',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './payment.component.html',
  styleUrls: ['./payment.component.css']
})
export class PaymentComponent implements OnInit {
  appointment: Appointment | null = null;
  tarif = 0;
  typeConsultation = '';
  
  isLoading = false;
  isProcessing = false;
  error = '';
  successMessage = '';
  
  paymentType: 'carte_bancaire' | 'carte_postale' = 'carte_bancaire';
  
  // Données de paiement
  paymentData = {
    // Carte bancaire
    numero_carte: '',
    nom_porteur: '',
    date_expiration: '',
    cvv: '',
    
    // Carte postale
    numero_ccp: '',
    cle_ccp: ''
  };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private paymentService: PaymentService,
    private appointmentService: AppointmentService
  ) {}

  ngOnInit() {
    const appointmentId = this.route.snapshot.params['id'];
    if (appointmentId) {
      this.loadAppointmentAndTarif(parseInt(appointmentId));
    } else {
      this.error = 'ID de rendez-vous manquant';
    }
  }

  loadAppointmentAndTarif(appointmentId: number) {
    this.isLoading = true;
    
    // Charger les détails du rendez-vous
    this.appointmentService.getAppointments().subscribe({
      next: (response) => {
        this.appointment = response.appointments.find(apt => apt.id === appointmentId) || null;
        
        if (!this.appointment) {
          this.error = 'Rendez-vous non trouvé';
          this.isLoading = false;
          return;
        }
        
        if (this.appointment.statut !== 'confirme') {
          this.error = 'Le rendez-vous doit être confirmé pour effectuer le paiement';
          this.isLoading = false;
          return;
        }
        
        // Charger le tarif
        this.loadTarif(appointmentId);
      },
      error: (error) => {
        this.error = 'Erreur lors du chargement du rendez-vous';
        this.isLoading = false;
      }
    });
  }

  loadTarif(appointmentId: number) {
    this.paymentService.getAppointmentTarif(appointmentId).subscribe({
      next: (response) => {
        this.tarif = response.tarif;
        this.typeConsultation = response.type_consultation;
        this.isLoading = false;
      },
      error: (error) => {
        this.error = 'Erreur lors du chargement du tarif';
        this.isLoading = false;
      }
    });
  }

  onPaymentTypeChange(type: 'carte_bancaire' | 'carte_postale') {
    this.paymentType = type;
    this.error = '';
  }

  onCardNumberInput(event: any) {
    let value = event.target.value.replace(/\s/g, '');
    value = value.replace(/(.{4})/g, '$1 ').trim();
    this.paymentData.numero_carte = value;
  }

  onExpiryInput(event: any) {
    let value = event.target.value.replace(/\D/g, '');
    if (value.length >= 2) {
      value = value.substring(0, 2) + '/' + value.substring(2, 4);
    }
    this.paymentData.date_expiration = value;
  }

  validateForm(): boolean {
    if (this.paymentType === 'carte_bancaire') {
      if (!this.paymentData.numero_carte || !this.paymentService.validateCardNumber(this.paymentData.numero_carte)) {
        this.error = 'Numéro de carte invalide';
        return false;
      }
      
      if (!this.paymentData.nom_porteur || this.paymentData.nom_porteur.trim().length < 2) {
        this.error = 'Nom du porteur requis';
        return false;
      }
      
      if (!this.paymentData.date_expiration || !this.paymentService.validateExpiryDate(this.paymentData.date_expiration)) {
        this.error = 'Date d\'expiration invalide';
        return false;
      }
      
      if (!this.paymentData.cvv || !this.paymentService.validateCVV(this.paymentData.cvv)) {
        this.error = 'CVV invalide';
        return false;
      }
    } else if (this.paymentType === 'carte_postale') {
      if (!this.paymentData.numero_ccp || !this.paymentService.validateCCP(this.paymentData.numero_ccp)) {
        this.error = 'Numéro CCP invalide';
        return false;
      }
      
      if (!this.paymentData.cle_ccp || !this.paymentService.validateCCPKey(this.paymentData.cle_ccp)) {
        this.error = 'Clé CCP invalide';
        return false;
      }
    }
    
    return true;
  }

  processPayment() {
    if (!this.validateForm() || !this.appointment) {
      return;
    }

    this.isProcessing = true;
    this.error = '';

    const paymentRequest: PaymentRequest = {
      rendez_vous_id: this.appointment.id,
      montant: this.tarif,
      type_paiement: this.paymentType
    };

    if (this.paymentType === 'carte_bancaire') {
      paymentRequest.numero_carte = this.paymentData.numero_carte.replace(/\s/g, '');
      paymentRequest.nom_porteur = this.paymentData.nom_porteur;
      paymentRequest.date_expiration = this.paymentData.date_expiration;
      paymentRequest.cvv = this.paymentData.cvv;
    } else {
      paymentRequest.numero_ccp = this.paymentData.numero_ccp;
      paymentRequest.cle_ccp = this.paymentData.cle_ccp;
    }

    this.paymentService.processPayment(paymentRequest).subscribe({
      next: (response) => {
        if (response.success) {
          this.successMessage = 'Paiement effectué avec succès !';
          setTimeout(() => {
            this.router.navigate(['/appointments']);
          }, 2000);
        } else {
          this.error = response.message;
        }
        this.isProcessing = false;
      },
      error: (error) => {
        this.error = error.error?.error || 'Erreur lors du traitement du paiement';
        this.isProcessing = false;
      }
    });
  }

  getCardType(): string {
    if (this.paymentData.numero_carte) {
      return this.paymentService.getCardType(this.paymentData.numero_carte);
    }
    return '';
  }

  formatAmount(amount: number): string {
    return this.paymentService.formatAmount(amount);
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

  goBack() {
    this.router.navigate(['/appointments']);
  }
}
